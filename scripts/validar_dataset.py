"""Valida envelope e coerência das fixtures, sem executar agentes ou validar LinkML."""
import json
from pathlib import Path
from datetime import datetime
from decimal import Decimal

ROOT = Path(__file__).resolve().parents[1]


def validar_schema(value, schema, path='$'):
    # Subconjunto usado pelo schema local; palavras desconhecidas falham explicitamente.
    supported = {'$schema', '$id', 'title', 'type', 'properties', 'required',
                 'additionalProperties', 'items', 'minItems', 'minLength', 'enum', 'const', 'anyOf'}
    assert not set(schema) - supported, (path, 'palavra de schema não suportada')
    if 'anyOf' in schema:
        for alternative in schema['anyOf']:
            try:
                validar_schema(value, alternative, path)
                return
            except AssertionError:
                pass
        raise AssertionError((path, 'nenhuma alternativa válida'))
    types = {'object': dict, 'array': list, 'string': str, 'boolean': bool, 'null': type(None)}
    if 'type' in schema:
        allowed = schema['type'] if isinstance(schema['type'], list) else [schema['type']]
        assert any(type(value) is types[t] for t in allowed), (path, 'tipo inválido')
    if 'enum' in schema:
        assert value in schema['enum'], (path, 'enum inválido')
    if 'const' in schema:
        assert type(value) is type(schema['const']) and value == schema['const'], (path, 'constante inválida')
    if isinstance(value, dict):
        assert not set(schema.get('required', [])) - set(value), (path, 'campo obrigatório ausente')
        props = schema.get('properties', {})
        if schema.get('additionalProperties') is False:
            assert not set(value) - set(props), (path, 'campo inesperado')
        for key, val in value.items():
            if key in props:
                validar_schema(val, props[key], path + '.' + key)
    if isinstance(value, list):
        assert len(value) >= schema.get('minItems', 0), (path, 'array curto')
        for i, val in enumerate(value):
            validar_schema(val, schema.get('items', {}), f'{path}[{i}]')
    if isinstance(value, str):
        assert len(value) >= schema.get('minLength', 0), (path, 'texto curto')


def validar():
    schema = json.loads((ROOT / 'src/evals/caso.schema.json').read_text())
    rows = [json.loads(line) for line in (ROOT / 'src/evals/casos.jsonl').read_text().splitlines() if line.strip()]
    ids = set()
    for row in rows:
        validar_schema(row, schema)
        cid = row['caso_id']
        assert cid not in ids, 'caso duplicado'
        ids.add(cid)
        e = row['entrada']
        assert cid == e['caso_id']
        for key in ['evidencias', 'regras']:
            keys = [x['id'] for x in e[key]]
            assert len(keys) == len(set(keys)), (cid, 'IDs duplicados', key)
        assert set(e['configuracao']['regras_aplicaveis']) == {r['id'] for r in e['regras']}
        instant = datetime.fromisoformat(e['instante_analise'])
        assert instant.tzinfo is not None
        for ev in e['evidencias']:
            when = datetime.fromisoformat(ev['disponivel_em'])
            assert when.tzinfo is not None and when <= instant
        d = e['dados']
        assert d['sinistro']['apolice'] == d['apolice']['id']
        assert d['apolice']['segurado'] == d['segurado']['id']
        assert d['apolice']['veiculo'] == d['veiculo']['id']
        assert d['orcamento']['sinistro'] == d['sinistro']['id']
        assert d['orcamento']['oficina'] == d['oficina']['id']
        assert d['sinistro']['possui_foto'] == bool(d['fotos'])
        for foto in d['fotos']:
            assert foto['sinistro'] == d['sinistro']['id']
        evidence_map = {'E-SIN':'sinistro','E-APO':'apolice','E-ORC':'orcamento','E-FOT':'fotos','E-CTX':'contexto_avaliacao'}
        for ev in e['evidencias']:
            assert ev['conteudo'] == d[evidence_map[ev['id']]], (cid, 'evidência divergente')
        for v in [d['sinistro']['valor_orcado'], d['orcamento']['valor']]:
            assert isinstance(v, str) and Decimal(v).is_finite() and Decimal(v) >= 0
        for expected in row['esperado'].values():
            assert expected['campos_iguais']['requer_decisao_humana'] is True
        rec = row['esperado']['recomendacao']['campos_iguais']
        assert rec['decisao_executada'] is False
        if rec['recomendacao'] == 'RECOMENDAR_APROVACAO':
            assert row['esperado']['documentacao']['campos_iguais']['situacao_documental'] == 'COMPLETA'
            assert row['esperado']['parecer']['campos_iguais']['analise_cobertura'] == 'SUSTENTADA_PELAS_REGRAS_FORNECIDAS'
            assert {r['id'] for r in e['regras']} >= {'R-DOC', 'R-COB', 'R-REC'}
            assert Decimal(d['sinistro']['valor_orcado']) <= Decimal('5000')
            assert d['contexto_avaliacao']['suspeita_fraude_confirmada_na_entrada'] is False
        if Decimal(d['sinistro']['valor_orcado']) > Decimal('5000'):
            assert all(ex['status_execucao'] == 'FORA_ESCOPO' for ex in row['esperado'].values())
        assert 'valor_recomendado' not in rec
        assert 'R-VAL' not in {r['id'] for r in e['regras']}
        assert e['configuracao']['versao_contrato'] == '0.2.0'
        # Lote sintético aprovado por Alex; regras permanecem simuladas.
        assert row['origem'] == 'SINTETICO' and row['particao'] == 'DESENVOLVIMENTO'
        assert not row['derivado_falha_observada']
        assert row['status_revisao'] == 'APROVADO_POR_ALEX'
        assert all(r['status'] == 'SIMULADA' for r in e['regras'])
    assert len(rows) == 30, 'lote de desenvolvimento deve ter 30 casos'
    assert ids == {f'FDE-{i:03}' for i in range(1, 31)}
    assert any(x['esperado']['triagem']['campos_iguais']['encaminhamento'] == 'REVISAO_ESPECIALIZADA' for x in rows)
    print(f'OK: {len(rows)} casos e {sum(len(r["esperado"]) for r in rows)} expectativas de módulos. Schema local e coerência verificados; nenhum agente executado.')


if __name__ == '__main__':
    validar()
