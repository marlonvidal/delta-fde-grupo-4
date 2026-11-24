"""Valida preparação do lote; --pronto bloqueia execução sem mídia e revisão."""
import argparse
import hashlib
import json
from pathlib import Path

P = Path(__file__).resolve().parents[1] / 'data/ampliacao-multimodal-v0'
def rows(name):
    return [json.loads(line) for line in (P / name).read_text().splitlines() if line.strip()]
def safe(name):
    path = (P / name).resolve()
    assert P.resolve() in path.parents, 'Referência fora do lote'
    return path

def validate(ready=False):
    entries, truth, docs, images = map(rows, ['entradas.jsonl','avaliador/verdade.jsonl','documentos/manifesto.jsonl','imagens/manifesto.jsonl'])
    assert len(entries)==len(truth)==10 and len(docs)==39 and len(images)==9
    expected_ids={f'MMV-{n:03}' for n in range(6,16)}
    assert {r['input']['caso_id'] for r in entries}=={r['caso_id'] for r in truth}==expected_ids
    assert len({d['documento_id'] for d in docs})==39
    targets={t['caso_id']:t for t in truth}
    by_image={i['caso_id']:i for i in images}
    for row in entries:
        inp=row['input']; cid=inp['caso_id']; target=targets[cid]['expectedOutput']
        assert inp==json.loads(safe(f'entradas/{cid}.json').read_text())
        assert not {'expectedOutput','gabarito','alvo_visual','titulo'} & inp.keys()
        assert row['metadata']['particao']=='DESENVOLVIMENTO'
        assert 'R-COB' not in {r['id'] for r in inp['regras']}
        inventory={d['documento_id']:d for d in docs if d['caso_id']==cid}
        assert {d['documento_id'] for d in inp['documentos']}==set(inventory)
        for d in inp['documentos']:
            file=safe(inventory[d['documento_id']]['arquivo'])
            assert file.read_text()==d['conteudo'] and 'SINTÉTIC' in d['conteudo']
            assert hashlib.sha256(file.read_bytes()).hexdigest()==inventory[d['documento_id']]['sha256']
        assert len(inp['imagens'])==(0 if cid=='MMV-015' else 1)
        if cid in by_image:
            image=by_image[cid]
            assert safe(image['prompt_arquivo']).is_file()
            assert inp['imagens'][0]['arquivo']==image['arquivo_esperado']
            if image['status']=='DISPONIVEL_REVISAO_HUMANA_PENDENTE':
                file=safe(image['arquivo_esperado'])
                assert file.read_bytes()[:8]==b'\x89PNG\r\n\x1a\n'
                assert hashlib.sha256(file.read_bytes()).hexdigest()==image['sha256']
            if ready:
                file=safe(image['arquivo_esperado'])
                assert file.is_file(), f'{cid}: imagem prevista não fornecida'
                assert hashlib.sha256(file.read_bytes()).hexdigest()==image['sha256']
                assert image['status']=='APROVADA_REVISAO_HUMANA'
        flow=target['fluxo_esperado']
        assert flow['decisao_humana_obrigatoria']
        assert not set(flow['modulos_previstos']) & set(flow['modulos_nao_executados'])
        assert flow['recomendacao_no_fluxo'] in [None,'RECOMENDAR_APROVACAO','REVISAO_HUMANA']
        assert (flow['rota']=='ANALISE_COMUM')==('parecer' in flow['modulos_previstos'])
        if ready:
            assert targets[cid]['metadata']['status_revisao']=='APROVADO_REVISAO_HUMANA'
    byid={e['input']['caso_id']:e['input'] for e in entries}
    def text(cid,kind):
        return next(d['conteudo'] for d in byid[cid]['documentos'] if d['tipo']==kind)
    assert all('5000.00' in text('MMV-006',k) for k in ['aviso','orcamento'])
    assert all('4999.99' in text('MMV-007',k) for k in ['aviso','orcamento'])
    assert not any(d['tipo']=='orcamento' for d in byid['MMV-008']['documentos'])
    assert 'INCOMPLETO' in text('MMV-009','orcamento')
    assert '2026-11-17' in text('MMV-010','apolice')
    assert 'Vigência inicial: 2026-11-18' in text('MMV-011','apolice')
    assert 'suspeita de fraude: sim' in text('MMV-014','aviso')
    assert '2300.00' in text('MMV-015','aviso') and '1800.00' in text('MMV-015','orcamento')
    assert targets['MMV-015']['expectedOutput']['fluxo_esperado']['rota']=='REVISAO_POR_INCERTEZA'
    print('OK: 10 casos, 39 documentos e 9 prompts consistentes. '+('Pronto para execução.' if ready else 'Rascunho validado; revisão humana pendente.'))

if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--pronto',action='store_true')
    validate(parser.parse_args().pronto)
