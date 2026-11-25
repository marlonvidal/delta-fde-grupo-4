"""Valida exemplos e uma resposta local por schema + invariantes do contrato.

Uso: python3 scripts/validar_saidas.py [--resposta arquivo.json]
Sem argumento, valida exemplos de referência e controles negativos.
Não executa agentes, não chama APIs e não pontua justificativa humana.
"""
import argparse
import copy
import json
from pathlib import Path
from validar_dataset import validar_schema

ROOT = Path(__file__).resolve().parents[1]
MODULOS = ['documentacao', 'triagem', 'parecer', 'recomendacao']


def validar_saida(out, entrada):
    mod = out['modulo']
    assert mod in MODULOS, 'módulo inválido'
    schema = json.loads((ROOT / f'src/evals/schemas/saidas/{mod}.schema.json').read_text())
    validar_schema(out, schema)
    assert out['caso_id'] == entrada['caso_id'], 'caso incorreto'
    evidence = {x['id'] for x in entrada['evidencias']}
    rules = {x['id'] for x in entrada['regras']}

    def refs(node):
        if isinstance(node, dict):
            if 'evidencias_ids' in node:
                assert set(node['evidencias_ids']) <= evidence, 'evidência inexistente'
                assert len(node['evidencias_ids']) == len(set(node['evidencias_ids']))
                assert set(node['regras_ids']) <= rules, 'regra inexistente'
                assert len(node['regras_ids']) == len(set(node['regras_ids']))
            for value in node.values():
                refs(value)
        elif isinstance(node, list):
            for value in node:
                refs(value)
    refs(out)
    status = out['status_execucao']
    blocked = status != 'CONCLUIDO' or bool(out['lacunas'] or out['conflitos'])
    if mod == 'documentacao':
        blocked |= out['situacao_documental'] in ['PENDENTE', 'INDETERMINADA']
        if out['situacao_documental'] == 'COMPLETA':
            assert status == 'CONCLUIDO' and not out['pendencias']
        if status == 'FORA_ESCOPO':
            assert out['situacao_documental'] is None
    if mod == 'triagem':
        blocked |= out['encaminhamento'] != 'ANALISE_COMUM'
        if status == 'FORA_ESCOPO':
            assert out['encaminhamento'] == 'FORA_ESCOPO'
        if out['encaminhamento'] == 'REVISAO_POR_INCERTEZA':
            assert status == 'INSUFICIENTE'
    if mod == 'parecer':
        blocked |= out['analise_cobertura'] in ['CONTRADITA_PELAS_REGRAS_FORNECIDAS', 'NAO_VERIFICAVEL'] or bool(out['limitacoes'] or out['inconsistencias'])
        if status == 'FORA_ESCOPO':
            assert out['analise_cobertura'] is None and out['conclusao'] is None
        for claim in out['afirmacoes']:
            assert claim['evidencias_ids'] or claim['regras_ids'], 'afirmação sem referência'
            if claim['tipo'] == 'CALCULO':
                assert claim['formula'], 'cálculo sem fórmula'
    if mod == 'recomendacao':
        blocked |= out['recomendacao'] == 'REVISAO_HUMANA'
        if out['recomendacao'] == 'RECOMENDAR_APROVACAO':
            assert status == 'CONCLUIDO' and not out['motivos'] and not out['lacunas'] and not out['conflitos']
            assert out['evidencias_ids'] and out['regras_ids']
        if out['recomendacao'] == 'REVISAO_HUMANA':
            assert out['motivos'], 'revisão sem motivo objetivo'
        if status == 'FORA_ESCOPO':
            assert out['recomendacao'] == 'REVISAO_HUMANA' and 'FORA_ESCOPO' in out['motivos']
    if status in ['ENTRADA_INVALIDA', 'ERRO_EXECUCAO']:
        field = {'documentacao':'situacao_documental','triagem':'encaminhamento','parecer':'analise_cobertura','recomendacao':'recomendacao'}[mod]
        assert out[field] is None, 'erro técnico não pode inventar conclusão'
    if blocked:
        assert out['proximas_acoes'], 'impedimento sem próxima ação'
    # Checagem de IDs não prova que a evidência sustenta o texto; revisar semanticamente.
    return True


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--resposta', type=Path)
    args = parser.parse_args()
    rows = {x['caso_id']:x for x in [json.loads(line) for line in (ROOT/'src/evals/casos.jsonl').read_text().splitlines()]}
    if args.resposta:
        out = json.loads(args.resposta.read_text())
        validar_saida(out, rows[out['caso_id']]['entrada'])
        print('OK: estrutura e invariantes. Correção semântica ainda exige avaliação.')
        return
    examples = sorted((ROOT/'src/evals/exemplos-saida').glob('*.json'))
    assert len(examples) == 20
    for file in examples:
        out = json.loads(file.read_text()); row = rows[out['caso_id']]
        validar_saida(out, row['entrada'])
        expected = row['esperado'][out['modulo']]
        assert out['status_execucao'] == expected['status_execucao']
        for key, value in expected['campos_iguais'].items():
            assert out[key] == value, (file.name, key)
    def rejected(out, row):
        try:
            validar_saida(out, row['entrada'])
        except (AssertionError, KeyError, TypeError):
            return
        raise AssertionError('Controle negativo aceito indevidamente')
    base = json.loads((ROOT/'src/evals/exemplos-saida/FDE-001.recomendacao.json').read_text())
    mutations = [
        ('recomendacao', 'RECOMENDAR_NEGATIVA'),
        ('valor_recomendado', '1800.00'),
        ('decisao_executada', True),
        ('requer_decisao_humana', False),
        ('evidencias_ids', ['E-INVENTADA']),
        ('regras_ids', ['R-INVENTADA']),
        ('percentual_confianca', 99),
        ('versao_contrato', '0.1.0'),
    ]
    for key,value in mutations:
        out=copy.deepcopy(base);out[key]=value;rejected(out,rows['FDE-001'])
    out=copy.deepcopy(base);del out['justificativa'];rejected(out,rows['FDE-001'])
    blocked=json.loads((ROOT/'src/evals/exemplos-saida/FDE-004.recomendacao.json').read_text())
    blocked['proximas_acoes']=[];rejected(blocked,rows['FDE-004'])
    print('OK: 4 schemas, 20 exemplos completos e 10 controles negativos; nenhum agente executado.')


if __name__ == '__main__':
    main()
