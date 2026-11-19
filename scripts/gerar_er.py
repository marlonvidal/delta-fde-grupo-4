#!/usr/bin/env python3
"""Gera o diagrama ER (Mermaid) da ontologia Amparo. Veja README.md."""
import argparse
import re
import subprocess
import sys
from pathlib import Path

import yaml

ONTOLOGIA = Path(__file__).resolve().parent.parent / "docs" / "ontologia"

# link_type -> (verbo, inverter)
ACOES = {
    "apolice_segurado":    ("contrata", True),
    "apolice_veiculo":     ("cobre", False),
    "renovacao_apolice":   ("renova", False),
    "sinistro_apolice":    ("aciona", False),
    "foto_sinistro":       ("documenta", False),
    "orcamento_sinistro":  ("orça o conserto de", False),
    "orcamento_oficina":   ("emite", True),
    "regulacao_sinistro":  ("analisa", False),
    "regulacao_analista":  ("realiza", True),
    "regulacao_orcamento": ("avalia", False),
    "pagamento_regulacao": ("autoriza", True),
    "pagamento_sinistro":  ("indeniza", False),
    "evento_sinistro":     ("registra etapa de", False),
    "score_sinistro":      ("avalia o risco de", False),
    "score_modelo":        ("gera", True),
    "auditoria_sinistro":  ("audita", False),
    "reclamacao_sinistro": ("contesta", False),
}

INVERTE_PONTA = {"}o": "o{", "}|": "|{", "||": "||", "|o": "o|", "o|": "|o", "o{": "}o", "|{": "}|"}

LINHA_RELACAO = re.compile(r'^\s*\S+\s+[|}o]{2}--[|{o]{2}\s+\S+\s*:\s*".*"\s*$')


def eh_object_type(defn):
    return (defn.get("annotations") or {}).get("foundry_kind") == "object_type"


def range_do_slot(schema, classe, slot):
    uso = (schema["classes"][classe].get("slot_usage") or {}).get(slot) or {}
    return uso.get("range") or (schema.get("slots", {}).get(slot) or {}).get("range")


def extrair_ligacoes(schema):
    ligacoes = []
    for classe, defn in schema["classes"].items():
        if not eh_object_type(defn):
            continue
        for slot, uso in (defn.get("slot_usage") or {}).items():
            anot = (uso or {}).get("annotations") or {}
            if "link_type" not in anot:
                continue
            destino = range_do_slot(schema, classe, slot)
            if destino not in schema["classes"]:
                print(f"aviso: {classe}.{slot} sem range de classe; ignorado", file=sys.stderr)
                continue
            ligacoes.append({
                "origem": classe,
                "destino": destino,
                "slot": slot,
                "nome": str(anot["link_type"]),
                "card": str(anot.get("cardinalidade", "N:1")).strip(),
                "inverso": anot.get("lado_inverso"),
                "obrigatorio": bool(uso.get("required")),
                "acao": anot.get("acao"),
            })
    return sorted(ligacoes, key=lambda l: l["nome"])


def simbolo(lig):
    um_destino = "||" if lig["obrigatorio"] else "o|"
    simbolos = {"N:1": "}o--" + um_destino, "1:N": "||--o{", "1:1": "|o--" + um_destino, "N:N": "}o--o{"}
    card = lig["card"].upper()
    if card not in simbolos:
        raise ValueError(f"cardinalidade desconhecida em {lig['origem']}.{lig['slot']}: {lig['card']}")
    return simbolos[card]


def inverter(sim):
    esq, dir_ = sim.split("--")
    return INVERTE_PONTA[dir_] + "--" + INVERTE_PONTA[esq]


def linha(lig, estilo):
    origem, destino, sim = lig["origem"], lig["destino"], simbolo(lig)
    texto = lig["nome"]
    if estilo == "nenhum":
        texto = ""
    elif estilo == "completo" and lig["inverso"]:
        texto = f'{lig["nome"]} ({lig["slot"]} / {lig["inverso"]})'
    elif estilo == "acao":
        verbo, inv = ACOES.get(lig["nome"], (lig["nome"], False))
        texto = str(lig["acao"]) if lig["acao"] else verbo
        if inv:
            origem, destino, sim = destino, origem, inverter(sim)
    return f'{origem} {sim} {destino} : "{texto}"'


def gerar_entidades(yaml_path, classes):
    cmd = ["gen-erdiagram", yaml_path, "--format", "mermaid", "--no-structural"]
    for c in classes:
        cmd += ["-c", c]
    saida = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8")
    if saida.returncode != 0:
        sys.exit("gen-erdiagram falhou:\n" + saida.stderr)
    return saida.stdout


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("schema", nargs="?", default=str(ONTOLOGIA / "amparo_core.yaml"))
    p.add_argument("-o", "--saida", default=str(ONTOLOGIA / "er.mmd"))
    p.add_argument("--layout", choices=["dagre", "elk"], default="elk")
    p.add_argument("--direcao", choices=["TB", "BT", "LR", "RL"])
    p.add_argument("--rotulo", choices=["simples", "completo", "nenhum", "acao"], default="acao")
    p.add_argument("--incluir-isolados", action="store_true")
    a = p.parse_args()

    with open(a.schema, encoding="utf-8") as f:
        schema = yaml.safe_load(f)
    ligacoes = extrair_ligacoes(schema)

    if a.incluir_isolados:
        classes = [c for c, d in schema["classes"].items() if eh_object_type(d)]
    else:
        nas_ligacoes = {l["origem"] for l in ligacoes} | {l["destino"] for l in ligacoes}
        classes = [c for c in schema["classes"] if c in nas_ligacoes]

    # mantém só as entidades do gen-erdiagram; as relações são refeitas abaixo
    corpo = [l for l in gerar_entidades(a.schema, classes).splitlines()
             if l.strip() and l.strip() != "erDiagram" and not LINHA_RELACAO.match(l)]

    linhas = ["---", "config:", f"  layout: {a.layout}", "---", "erDiagram"]
    if a.direcao:
        linhas.append(f"direction {a.direcao}")
    linhas += corpo + [""] + [linha(lig, a.rotulo) for lig in ligacoes]

    with open(a.saida, "w", encoding="utf-8") as f:
        f.write("\n".join(linhas) + "\n")

    print(f"{a.saida}: {len(classes)} object types, {len(ligacoes)} link types")
    for lig in ligacoes:
        print(f'  {lig["nome"]:<22} {lig["origem"]}.{lig["slot"]} -> {lig["destino"]}  [{lig["card"]}]')


if __name__ == "__main__":
    main()
