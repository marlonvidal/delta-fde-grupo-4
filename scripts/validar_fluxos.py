"""Checa snapshots sintéticos integrados. Não executa agente ou pagamento."""
import copy
import hashlib
import json
from datetime import datetime
from decimal import Decimal, InvalidOperation
from validar_dataset import ROOT, validar_schema
from validar_saidas import validar_saida, MODULOS


def hash_entrada(entrada):
    return hashlib.sha256(json.dumps(entrada, ensure_ascii=False, sort_keys=True, separators=(',', ':')).encode()).hexdigest()


def precondicoes_pagamento_sintetico(snapshot):
    """Somente predicado de teste; não verifica identidade/autenticidade nem autoriza transação real."""
    h = snapshot['decisao_humana']
    if not h or snapshot['rota'] == 'FALHA_TECNICA':
        return False
    try:
        valor = Decimal(h['valor_aprovado_humano'])
    except (TypeError, InvalidOperation):
        return False
    return (h['origem'] == 'REGISTRO_HUMANO' and h['acao'] == 'APROVAR'
            and h['execucao_id'] == snapshot['execucao_id']
            and h['entrada_sha256'] == snapshot['entrada_sha256']
            and valor.is_finite() and Decimal('0') < valor <= Decimal('5000'))


def validar_snapshot(out, entrada):
    schema = json.loads((ROOT/'src/evals/schemas/painel.schema.json').read_text())
    validar_schema(out, schema)
    assert out['caso_id'] == entrada['caso_id']
    assert out['entrada_sha256'] == hash_entrada(entrada)
    assert datetime.fromisoformat(out['gerado_em']) >= datetime.fromisoformat(entrada['instante_analise'])
    assert set(out['evidencias_ids']) <= {x['id'] for x in entrada['evidencias']}
    assert set(out['regras_ids']) <= {x['id'] for x in entrada['regras']}
    action = out['proxima_acao']
    assert set(action['evidencias_ids']) <= {x['id'] for x in entrada['evidencias']}
    assert set(action['regras_ids']) <= {x['id'] for x in entrada['regras']}
    modules=out['modulos']
    failed=False
    for mod in MODULOS:
        stage=modules[mod]
        if stage['estado']=='NAO_EXECUTADO':
            assert stage['saida'] is None and stage['motivo_nao_execucao']
        else:
            assert stage['saida'] is not None and stage['motivo_nao_execucao'] is None
            assert stage['saida']['modulo']==mod
            validar_saida(stage['saida'],entrada)
            is_error=stage['saida']['status_execucao'] in ['ERRO_EXECUCAO','ENTRADA_INVALIDA']
            assert (stage['estado']=='FALHA')==is_error
            assert not failed, 'módulo executado após falha anterior'
            failed |= is_error
    assert modules['documentacao']['estado']!='NAO_EXECUTADO'
    if modules['documentacao']['estado']=='FALHA':
        assert modules['triagem']['estado']=='NAO_EXECUTADO'
    else:
        assert modules['triagem']['estado']!='NAO_EXECUTADO'
    route=out['rota']
    if failed:
        assert route=='FALHA_TECNICA'
    else:
        assert route==modules['triagem']['saida']['encaminhamento']
    if route=='ANALISE_COMUM':
        assert all(s['estado']=='EXECUTADO' for s in modules.values())
    elif not failed:
        assert all(modules[m]['estado']=='NAO_EXECUTADO' for m in ['parecer','recomendacao'])
        for m in ['parecer','recomendacao']:
            assert modules[m]['motivo_nao_execucao']=='DESVIO_DE_ROTA'
    if failed:
        for stage in modules.values():
            if stage['estado']=='NAO_EXECUTADO':
                assert stage['motivo_nao_execucao']=='FALHA_ANTERIOR'
    expected={
        'ANALISE_COMUM':('AGUARDANDO_ANALISTA','REVISAR_E_DECIDIR'),
        'COMPLEMENTACAO_DOCUMENTAL':('AGUARDANDO_SOLICITACAO_COMPLEMENTO','SOLICITAR_COMPLEMENTO'),
        'REVISAO_ESPECIALIZADA':('AGUARDANDO_ENCAMINHAMENTO_ESPECIALISTA','ENCAMINHAR_ESPECIALISTA'),
        'REVISAO_POR_INCERTEZA':('AGUARDANDO_ANALISE_MANUAL','ENCAMINHAR_ANALISE_MANUAL'),
        'FORA_ESCOPO':('AGUARDANDO_ANALISE_MANUAL','ENCAMINHAR_ANALISE_MANUAL'),
        'FALHA_TECNICA':('FALHA_TECNICA','CORRIGIR_E_REPROCESSAR')}
    h=out['decisao_humana']
    if h:
        assert h['execucao_id']==out['execucao_id'] and h['entrada_sha256']==out['entrada_sha256']
        assert datetime.fromisoformat(h['registrada_em'])>=datetime.fromisoformat(out['gerado_em'])
        if h['acao']=='APROVAR':
            assert precondicoes_pagamento_sintetico(out)
            assert out['situacao_painel']=='DECISAO_HUMANA_REGISTRADA'
            assert action['codigo']=='REGISTRAR_NO_SISTEMA'
        else:
            assert h['valor_aprovado_humano'] is None
            human_map={'ENCAMINHAR_ANALISE_MANUAL':('AGUARDANDO_ANALISE_MANUAL','ENCAMINHAR_ANALISE_MANUAL'),
                       'SOLICITAR_COMPLEMENTO':('AGUARDANDO_SOLICITACAO_COMPLEMENTO','SOLICITAR_COMPLEMENTO'),
                       'ENCAMINHAR_ESPECIALISTA':('AGUARDANDO_ENCAMINHAMENTO_ESPECIALISTA','ENCAMINHAR_ESPECIALISTA')}
            assert (out['situacao_painel'],action['codigo'])==human_map[h['acao']]
    else:
        assert (out['situacao_painel'],action['codigo'])==expected[route]
    return True


def validar_historico(out, entrada, historico):
    prior=out['execucao_anterior_id']
    if not prior:
        assert out['versao_entrada']=='1'
        return
    assert prior in historico, 'execução anterior inexistente'
    old=historico[prior]
    assert old['caso_id']==out['caso_id']
    assert int(out['versao_entrada'])>int(old['versao_entrada'])
    assert out['entrada_sha256']!=old['entrada_sha256'], 'nova versão sem mudança de entrada'
    assert datetime.fromisoformat(out['gerado_em'])>datetime.fromisoformat(old['gerado_em'])
    assert out['decisao_humana'] is None, 'decisão antiga não pode ser copiada para nova análise'


def main():
    cases=[json.loads(x) for x in (ROOT/'src/evals/integrados/casos.jsonl').read_text().splitlines()]
    assert len(cases)==10
    history={};seen=set()
    for case in cases:
        assert case['fluxo_id'] not in seen;seen.add(case['fluxo_id'])
        out=case['snapshot_esperado'];entry=case['entrada']
        validar_snapshot(out,entry);validar_historico(out,entry,history)
        assert precondicoes_pagamento_sintetico(out)==case['controle_pagamento_esperado']
        assert out==json.loads((ROOT/f"src/evals/integrados/exemplos/{case['fluxo_id']}.painel.json").read_text())
        assert out['execucao_id'] not in history;history[out['execucao_id']]=out
    def rejected(out, entry):
        try:
            validar_snapshot(out,entry)
        except (AssertionError,TypeError,KeyError):
            return
        raise AssertionError('controle negativo aceito')
    blocked=cases[1];base=cases[0]
    bad=copy.deepcopy(blocked['snapshot_esperado']);bad['modulos']['parecer']=copy.deepcopy(base['snapshot_esperado']['modulos']['parecer']);rejected(bad,blocked['entrada'])
    bad=copy.deepcopy(blocked['snapshot_esperado']);bad['modulos']['recomendacao']['saida']=copy.deepcopy(base['snapshot_esperado']['modulos']['recomendacao']['saida']);rejected(bad,blocked['entrada'])
    for field,value in [('entrada_sha256','hash-antigo'),('pagamento_executado_pelo_agente',True),('rota','ANALISE_COMUM')]:
        bad=copy.deepcopy(blocked['snapshot_esperado']);bad[field]=value;rejected(bad,blocked['entrada'])
    bad=copy.deepcopy(blocked['snapshot_esperado']);bad['proxima_acao']['codigo']='ENCAMINHAR_ANALISE_MANUAL';rejected(bad,blocked['entrada'])
    approved=cases[8]
    for field,value in [('execucao_id','RUN-ANTIGA'),('entrada_sha256','hash-antigo'),('origem','MODELO_IA')]:
        bad=copy.deepcopy(approved['snapshot_esperado']);bad['decisao_humana'][field]=value
        assert not precondicoes_pagamento_sintetico(bad)
        rejected(bad,approved['entrada'])
    # Retomada obsoleta e histórico inexistente também devem falhar.
    for prior in ['RUN-INEXISTENTE','RUN-INT-003']:
        bad=copy.deepcopy(cases[5]['snapshot_esperado']);bad['execucao_anterior_id']=prior
        try:validar_historico(bad,cases[5]['entrada'],history)
        except AssertionError:pass
        else:raise AssertionError('histórico inválido aceito')
    assert cases[7]['snapshot_esperado']['modulos']==base['snapshot_esperado']['modulos'], 'discordância alterou sugestão original'
    print('OK: 10 cenários integrados, 10 snapshots, 11 controles negativos; nenhum agente ou pagamento executado.')


if __name__=='__main__':main()
