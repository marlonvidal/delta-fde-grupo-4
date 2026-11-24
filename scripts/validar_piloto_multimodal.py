"""Confere lote local sem criar imagens, chamar modelo ou acessar Langfuse."""
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
P = ROOT / 'data/piloto-multimodal-v0'


def read_rows(path):
    return [json.loads(x) for x in path.read_text().splitlines() if x.strip()]


def local_path(name):
    p = (P / name).resolve()
    assert P.resolve() in p.parents, 'referência fora do lote'
    return p


def main():
    docs=read_rows(P/'documentos/manifesto.jsonl')
    images=read_rows(P/'imagens/manifesto.jsonl')
    entries=read_rows(P/'entradas.jsonl')
    truth=read_rows(P/'avaliador/verdade.jsonl')
    assert len(docs)==19 and len(images)==4 and len(entries)==len(truth)==5
    ids={f'FDE-{i:03}' for i in range(1,6)}
    assert {x['input']['caso_id'] for x in entries}==ids
    assert {x['caso_id'] for x in truth}==ids
    assert len({x['documento_id'] for x in docs})==19
    for d in docs:
        p=local_path(d['arquivo'])
        assert p.is_file()
        assert hashlib.sha256(p.read_bytes()).hexdigest()==d['sha256']
        assert 'SINTÉTIC' in p.read_text()
    by_case={x['caso_id']:x for x in truth}
    for row in entries:
        entry=row['input'];cid=entry['caso_id']
        assert set(row)=={'input','metadata'}
        assert not {'expectedOutput','esperado','gabarito','tipo_dano_alvo','qualidade_foto'} & entry.keys()
        assert 'tipo_dano' not in entry['contexto'] and 'qualidade_foto' not in entry['contexto']
        assert entry==json.loads((P/f'entradas/{cid}.json').read_text())
        actual={d['documento_id']:d for d in docs if d['caso_id']==cid}
        assert len(entry['documentos'])==(3 if cid=='FDE-004' else 4)
        assert {d['documento_id'] for d in entry['documentos']}==set(actual)
        for d in entry['documentos']:
            assert d['conteudo']==local_path(actual[d['documento_id']]['arquivo']).read_text()
        assert 'R-COB' not in {r['id'] for r in entry['regras']}, 'cobertura deve vir somente do documento disponível'
        if cid=='FDE-004':
            assert not any(d['tipo']=='condicoes' for d in entry['documentos'])
        if cid=='FDE-002':
            assert not entry['imagens']
        else:
            assert len(entry['imagens'])==1
            img=next(i for i in images if i['caso_id']==cid)
            assert entry['imagens'][0]['arquivo']==img['arquivo_esperado']
            assert img['status']=='DISPONIVEL_REVISAO_HUMANA_PENDENTE' and img['sha256']
            photo=local_path(img['arquivo_esperado'])
            assert photo.is_file() and photo.read_bytes()[:8]==b'\x89PNG\r\n\x1a\n'
            assert hashlib.sha256(photo.read_bytes()).hexdigest()==img['sha256']
            assert local_path(img['prompt_arquivo']).is_file()
        expected=by_case[cid]
        assert expected['metadata']['status_revisao']=='PENDENTE_REVISAO_MULTIMODAL'
        flow=expected['expectedOutput']['fluxo_esperado']
        assert flow['decisao_humana_obrigatoria'] is True
        assert ('parecer' in flow['modulos_previstos'])==(flow['rota']=='ANALISE_COMUM')
        assert not set(flow['modulos_previstos']) & set(flow['modulos_nao_executados'])
    # Invariantes dos cenários de divergência e limite.
    for cid,amount,budget in [('FDE-003','2300.00','1800.00'),('FDE-005','5000.01','5000.01')]:
        assert amount in (P/f'documentos/{cid}/aviso.txt').read_text()
        assert budget in (P/f'documentos/{cid}/orcamento.txt').read_text()
    assert len(list((P/'imagens').glob('*.png')))==4
    assert len({x['sha256'] for x in images})==4, 'arquivos repetidos'
    manifest=json.loads((P/'manifesto.json').read_text())
    assert manifest['imagens_presentes']==4
    if manifest['upload_langfuse_realizado']:
        assert manifest['langfuse']['dataset_id'] and manifest['langfuse']['verificado_em']
    print('OK: 5 casos, 19 documentos consistentes, gabarito separado e 4 imagens recebidas com hashes válidos. Revisão humana pendente; nenhuma execução multimodal do agente.')


if __name__=='__main__':main()
