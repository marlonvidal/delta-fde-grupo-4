"""Audita contratos de ingestão e rastreabilidade; não executa extrator ou agente."""
import copy
import json
import re
from datetime import datetime
from pathlib import Path
from validar_dataset import validar_schema

R = Path(__file__).resolve().parents[1]

def load(name):
    return json.loads((R/name).read_text())
def instant(value):
    dt=datetime.fromisoformat(value)
    assert dt.tzinfo is not None, 'instante sem fuso'
    return dt

def validar_evento(event):
    validar_schema(event,load('src/evals/schemas/chat-anexos.schema.json'))
    when=instant(event['instante_recebimento'])
    assert len({a['anexo_id'] for a in event['anexos']})==len(event['anexos']), 'anexo duplicado'
    for a in event['anexos']:
        assert re.fullmatch('[0-9a-f]{64}',a['sha256']), 'hash inválido'
        assert instant(a['recebido_em'])<=when, 'evidência posterior ao evento'
        assert a['tamanho_bytes']>0, 'arquivo vazio'
    return True

def validar_ingestao(out,event):
    validar_evento(event)
    validar_schema(out,load('src/evals/schemas/resultado-ingestao.schema.json'))
    for field in ['evento_id','caso_id','versao_entrada']:
        assert out[field]==event[field], 'resultado de evento/versão diferente'
    assert instant(out['processado_em'])>=instant(event['instante_recebimento'])
    assert len(out['anexos'])==len(event['anexos'])
    assert {a['anexo_id'] for a in out['anexos']}=={a['anexo_id'] for a in event['anexos']}
    assert len({a['anexo_id'] for a in out['anexos']})==len(out['anexos'])
    evidence=[]
    for a in out['anexos']:
        if a['status_processamento']=='PROCESSADO':
            assert a['texto_extraido'] or a['campos_extraidos'], 'extração vazia apresentada como processada'
            assert a['evidencias'], 'extração sem proveniência'
            assert a['erro_codigo'] is None and a['motivo'] is None
            evidence.extend(e['id'] for e in a['evidencias'])
        else:
            assert a['erro_codigo'] and a['motivo'], 'falha sem motivo'
            assert a['texto_extraido'] is None and not a['campos_extraidos'] and not a['evidencias'], 'falha apresentada como extração válida'
    assert len(evidence)==len(set(evidence)), 'IDs de evidência repetidos'
    return True

def validar_matriz():
    matrix=load('src/evals/ingestao/rastreabilidade-15-casos.json')
    assert len(matrix)==15 and len({r['caso_id'] for r in matrix})==15
    for row in matrix:
        e=load(row['fonte_entrada']);cid=row['caso_id']
        reference=next(x for x in map(json.loads,(R/row['fonte_gabarito']).read_text().splitlines()) if x['caso_id']==cid)
        truth=reference['expectedOutput']
        manifest=load(str(Path(row['fonte_gabarito']).parents[1]/'manifesto.json'))
        assert manifest['versao_gabarito']==reference['metadata']['versao_gabarito'], 'manifesto/gabarito de versões diferentes'
        assert reference['metadata']['status_revisao']=='APROVADO_REVISAO_HUMANA'
        assert reference['metadata']['aceite_visual_documental']['responsavel']=='Alex'
        flow=truth['fluxo_esperado']
        assert row['documentos_ids']==[d['documento_id'] for d in e['documentos']]
        assert row['imagens_ids']==[d['imagem_id'] for d in e['imagens']]
        assert row['regras_operacionais']==[r['id'] for r in e['regras']]
        assert row['fonte_cobertura']==next((d['documento_id'] for d in e['documentos'] if d['tipo']=='condicoes'),None)
        for key,field in [('rota','rota'),('executados','modulos_previstos'),('nao_executados','modulos_nao_executados'),('recomendacao_fluxo','recomendacao_no_fluxo')]:
            assert row[key]==flow[field]
        assert set(row['executados']).isdisjoint(row['nao_executados'])
        assert ('parecer' in row['executados'])==(row['rota']=='ANALISE_COMUM')
        for module in row['executados']:
            criteria=truth['criterios_por_modulo'][module]
            assert criteria.get('status_execucao') is not None, 'status por módulo ausente após consolidação'
            assert row['status_gabarito'][module]==criteria['status_execucao']
            if row['status_gabarito'][module] is not None:
                assert row['status_proposto'][module]==row['status_gabarito'][module]
            props=load(f'src/evals/schemas/saidas/{module}.schema.json')['properties']
            validar_schema(row['status_proposto'][module],props['status_execucao'])
            for field,value in criteria['campos_iguais'].items():
                assert field in props
                validar_schema(value,props[field])
        if row['rota']=='REVISAO_POR_INCERTEZA':assert row['status_proposto']['triagem']=='INSUFICIENTE'
        if row['recomendacao_fluxo']=='RECOMENDAR_APROVACAO':
            assert row['situacao_documental']=='COMPLETA'
            assert truth['criterios_por_modulo']['parecer']['campos_iguais']['analise_cobertura']=='SUSTENTADA_PELAS_REGRAS_FORNECIDAS'
    old=[json.loads(line) for line in (R/'src/evals/casos.jsonl').read_text().splitlines()]
    assert {case['versao_dataset'] for case in old}=={'0.3.1'}
    for case in old:
        if case['caso_id'] in ['FDE-017','FDE-018']:
            assert case['esperado']['triagem']['campos_iguais']['encaminhamento']=='ANALISE_COMUM'
            assert case['esperado']['recomendacao']['campos_iguais']['recomendacao']=='REVISAO_HUMANA'
    assert next(x for x in matrix if x['caso_id']=='FDE-004')['fonte_cobertura'] is None
    assert next(x for x in matrix if x['caso_id']=='MMV-015')['rota']=='REVISAO_POR_INCERTEZA'
    assert next(x for x in matrix if x['caso_id']=='MMV-010')['recomendacao_fluxo']=='REVISAO_HUMANA'
    contract=(R/'docs/contratos/01-documentacao.md').read_text().split('## Entrada documental')[0]
    assert '`criterio_id`' in contract and '`requisito_id`' not in contract
    return matrix

def main():
    event=load('src/evals/ingestao/entrada-chat.json');out=load('src/evals/ingestao/resultado-processado.json');error=load('src/evals/ingestao/resultado-falha.json')
    validar_ingestao(out,event);validar_ingestao(error,event)
    empty=copy.deepcopy(event);empty['anexos']=[];validar_evento(empty)
    for status in ['ILEGIVEL','NAO_SUPORTADO','PROTEGIDO','CORROMPIDO']:
        failure=copy.deepcopy(error);failure['anexos'][0]['status_processamento']=status;validar_ingestao(failure,event)
    negatives=[]
    for kind in ['hash','futuro','fuso','duplicado','bytes_boolean','campo_extra']:
        bad=copy.deepcopy(event)
        if kind=='hash':bad['anexos'][0]['sha256']='arquivo.png'
        if kind=='futuro':bad['anexos'][0]['recebido_em']='2099-01-01T00:00:00+00:00'
        if kind=='fuso':bad['instante_recebimento']='2026-11-20T10:00:00'
        if kind=='duplicado':bad['anexos'].append(copy.deepcopy(bad['anexos'][0]))
        if kind=='bytes_boolean':bad['anexos'][0]['tamanho_bytes']=True
        if kind=='campo_extra':bad['aprovado']=True
        negatives.append((validar_evento,[bad]))
    for kind in ['sem_origem','versao_antiga','anexo_errado','falha_com_texto','falha_sem_motivo','sucesso_vazio','estado_inventado']:
        bad=copy.deepcopy(out if kind not in ['falha_com_texto','falha_sem_motivo'] else error)
        if kind=='sem_origem':bad['anexos'][0]['evidencias']=[]
        if kind=='versao_antiga':bad['versao_entrada']=2
        if kind=='anexo_errado':bad['anexos'][0]['anexo_id']='outro-anexo'
        if kind=='falha_com_texto':bad['anexos'][0]['texto_extraido']='Apólice vigente'
        if kind=='falha_sem_motivo':bad['anexos'][0]['motivo']=None
        if kind=='sucesso_vazio':bad['anexos'][0].update(texto_extraido=None,campos_extraidos={})
        if kind=='estado_inventado':bad['anexos'][0]['status_processamento']='APROVADO'
        negatives.append((validar_ingestao,[bad,event]))
    for fn,args in negatives:
        try:fn(*args)
        except AssertionError:pass
        else:raise AssertionError('controle negativo aceito indevidamente')
    matrix=validar_matriz();invalid=copy.deepcopy(out);invalid['anexos'][0]['evidencias'][0]['localizador']=''
    try:validar_ingestao(invalid,event)
    except AssertionError:pass
    else:raise AssertionError('localizador vazio aceito')
    print(f'OK: 2 schemas de ingestão, exemplos e estados, {len(negatives)+1} controles negativos e rastreabilidade de {len(matrix)} casos. Nenhum agente/OCR executado.')

if __name__=='__main__':main()
