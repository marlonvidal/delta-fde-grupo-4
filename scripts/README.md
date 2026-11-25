# gerar_er.py

Gera o diagrama ER (Mermaid) da ontologia Amparo a partir do schema LinkML
(`docs/ontologia/amparo_core.yaml`), com os nomes de relação e as cardinalidades
corretas.

O `gen-erdiagram` do LinkML rotula cada ligação com o nome do slot (ex.: `apolice`)
e deduz a cardinalidade apenas de `required`/`multivalued`. Este script aproveita as
entidades geradas pelo `gen-erdiagram`, descarta as ligações dele e as refaz a partir
das annotations do schema:

| Annotation / campo | Uso no diagrama                                   |
|--------------------|---------------------------------------------------|
| `link_type`        | nome da relação (ex.: `sinistro_apolice`)         |
| `cardinalidade`    | `N:1` (padrão), `1:N`, `1:1` ou `N:N`             |
| `required`         | lado "um" obrigatório (`\|\|`) ou opcional (`o\|`) |
| `lado_inverso`     | usado no rótulo `--rotulo completo`               |
| `acao`             | verbo usado no rótulo `--rotulo acao`             |

Só entram classes com `annotations.foundry_kind: object_type`. O `range` da
ligação vem do `slot_usage` da classe ou, se não houver, da definição global
do slot em `slots`.

Conectores Mermaid gerados (lado esquerdo = origem, lado direito = destino):

| Cardinalidade | `required: true` | `required: false` |
|---------------|------------------|-------------------|
| `N:1`         | `}o--\|\|`       | `}o--o\|`         |
| `1:N`         | `\|\|--o{`       | `\|\|--o{`        |
| `1:1`         | `\|o--\|\|`      | `\|o--o\|`        |
| `N:N`         | `}o--o{`         | `}o--o{`          |

## 1. Pré-requisitos

- **Python 3.9+** (testado com 3.14)
- **pip** (vem junto com o Python)
- **Node.js 18+**, opcional, só para converter o `.mmd` em PDF/PNG/SVG

### Instalando o Python

macOS (Homebrew):

```bash
brew install python
python3 --version
```

Linux (Debian/Ubuntu):

```bash
sudo apt update && sudo apt install python3 python3-venv python3-pip
```

Windows: baixe o instalador em <https://www.python.org/downloads/> e marque
"Add Python to PATH" durante a instalação.

## 2. Ambiente virtual e dependências

Na raiz do repositório:

```bash
python3 -m venv .venv
source .venv/bin/activate          # Windows: .venv\Scripts\activate
pip install --upgrade pip
pip install -r scripts/requirements.txt
```

- `linkml` fornece o comando `gen-erdiagram`, que o script chama via subprocess.
- `pyyaml` é usado para ler o schema.

Confira se ficou tudo no PATH:

```bash
gen-erdiagram --help
```

Se aparecer `command not found`, ative o ambiente virtual de novo
(`source .venv/bin/activate`).

### Opcional: Mermaid CLI (para exportar PDF/PNG/SVG)

```bash
npm install -g @mermaid-js/mermaid-cli
mmdc --version
```

O `mmdc` usa um Chrome headless via puppeteer. Versões recentes do npm bloqueiam
o script que baixa esse navegador (aviso `install scripts blocked ... puppeteer`),
e o `mmdc` falha em `ChromeLauncher.launch`. Nesse caso, baixe o navegador à mão:

```bash
cd "$(npm root -g)/@mermaid-js/mermaid-cli" && npx puppeteer browsers install chrome-headless-shell
```

## 3. Uso

Na raiz do repositório, sem argumentos:

```bash
python scripts/gerar_er.py
```

Isso lê `docs/ontologia/amparo_core.yaml` e grava `docs/ontologia/er.mmd`. Os
caminhos padrão são relativos ao repositório, então o comando funciona de
qualquer pasta.

Saída esperada:

```
.../docs/ontologia/er.mmd: 15 object types, 17 link types
  apolice_segurado       Apolice.segurado -> Segurado  [N:1]
  apolice_veiculo        Apolice.veiculo -> Veiculo  [N:1]
  ...
```

### Opções

| Opção                 | Valores                                      | Padrão          | Descrição |
|-----------------------|----------------------------------------------|-----------------|-----------|
| `schema` (posicional) | caminho do YAML                              | `docs/ontologia/amparo_core.yaml` | Schema LinkML da ontologia |
| `-o`, `--saida`       | caminho do `.mmd`                            | `docs/ontologia/er.mmd` | Arquivo Mermaid gerado |
| `--layout`            | `elk`, `dagre`                               | `elk`           | Motor de layout do Mermaid |
| `--direcao`           | `TB`, `BT`, `LR`, `RL`                       | (nenhuma)       | Direção do diagrama |
| `--rotulo`            | `simples`, `completo`, `nenhum`, `acao`      | `acao`          | Texto exibido nas ligações |
| `--incluir-isolados`  | flag                                         | desligado       | Inclui object types sem ligações (ex.: `RegraNegocio`, `SistemaFonte`, `AvaliacaoBloco`) |

Estilos de `--rotulo`:

- `simples`: o `link_type` (ex.: `sinistro_apolice`)
- `completo`: `link_type (slot / lado_inverso)`, quando há `lado_inverso`
- `nenhum`: ligações sem texto
- `acao`: verbo de negócio (ex.: `Sinistro aciona Apolice`). Vem da annotation
  `acao` no `slot_usage` do YAML; se não existir, do dicionário `ACOES` no script.
  Ações marcadas com `inverter = True` são lidas do destino para a origem
  (ex.: `Oficina emite Orcamento`), e a linha é desenhada invertida.
  Um `link_type` sem ação definida usa o próprio nome como rótulo.

Ações padrão (dicionário `ACOES`):

| `link_type`           | Leitura no diagrama                       | Invertida |
|-----------------------|-------------------------------------------|-----------|
| `apolice_segurado`    | Segurado **contrata** Apolice             | sim       |
| `apolice_veiculo`     | Apolice **cobre** Veiculo                 | não       |
| `renovacao_apolice`   | Apolice **renova** Apolice anterior       | não       |
| `sinistro_apolice`    | Sinistro **aciona** Apolice               | não       |
| `foto_sinistro`       | FotoDano **documenta** Sinistro           | não       |
| `orcamento_sinistro`  | Orcamento **orça o conserto de** Sinistro | não       |
| `orcamento_oficina`   | Oficina **emite** Orcamento               | sim       |
| `regulacao_sinistro`  | Regulacao **analisa** Sinistro            | não       |
| `regulacao_analista`  | AnalistaRegulacao **realiza** Regulacao   | sim       |
| `regulacao_orcamento` | Regulacao **avalia** Orcamento            | não       |
| `pagamento_regulacao` | Regulacao **autoriza** Pagamento          | sim       |
| `pagamento_sinistro`  | Pagamento **indeniza** Sinistro           | não       |
| `evento_sinistro`     | EventoSinistro **registra etapa de** Sinistro | não   |
| `score_sinistro`      | ScoreFraude **avalia o risco de** Sinistro | não      |
| `score_modelo`        | ModeloAnalitico **gera** ScoreFraude      | sim       |
| `auditoria_sinistro`  | AuditoriaFraude **audita** Sinistro       | não       |
| `reclamacao_sinistro` | Reclamacao **contesta** Sinistro          | não       |

### Exemplos

O comando sem opções gera o `er.mmd` usado no `er.pdf` da entrega. Para
variações, use `-o` com outro nome e não sobrescreva o `er.mmd`:

```bash
# layout ELK, da esquerda para a direita
python scripts/gerar_er.py -o docs/ontologia/er_lr.mmd --direcao LR

# rótulo = link_type, ou link_type com o lado inverso
python scripts/gerar_er.py -o docs/ontologia/er_link_types.mmd --rotulo simples
python scripts/gerar_er.py -o docs/ontologia/er_completo.mmd --rotulo completo

# incluindo entidades sem ligação
python scripts/gerar_er.py -o docs/ontologia/er_isolados.mmd --incluir-isolados

# sem rótulos
python scripts/gerar_er.py -o docs/ontologia/er_sem_rotulos.mmd --rotulo nenhum

# outro schema
python scripts/gerar_er.py caminho/outro_schema.yaml -o caminho/outro_er.mmd
```

## 4. Exportando o diagrama

Com o Mermaid CLI instalado, na raiz do repositório:

```bash
mmdc -i docs/ontologia/er.mmd -o docs/ontologia/er.pdf -t neutral
mmdc -i docs/ontologia/er.mmd -o docs/ontologia/er.svg -t neutral
mmdc -i docs/ontologia/er.mmd -o docs/ontologia/er.png -t neutral -s 2   # -s = escala
```

O `er.mmd` e o `er.pdf` ficam versionados em `docs/ontologia/`. Ao mudar o
`amparo_core.yaml`, rode o script e o `mmdc` de novo e versione os dois arquivos.

Sem instalar nada, dá para colar o conteúdo do `.mmd` em
<https://mermaid.live> para visualizar.

## 5. Adicionando ou ajustando uma relação

No YAML, dentro do `slot_usage` da classe de origem:

```yaml
classes:
  Sinistro:
    annotations:
      foundry_kind: object_type
    slot_usage:
      apolice:
        range: Apolice
        required: true
        annotations:
          link_type: sinistro_apolice
          cardinalidade: "N:1"
          lado_inverso: sinistros
          acao: aciona            # opcional; sobrepõe o dicionário ACOES
```

Para mudar o verbo ou o sentido de leitura sem mexer no schema, edite o
dicionário `ACOES` no início de `gerar_er.py`.

## 6. Problemas comuns

| Mensagem | Causa / solução |
|----------|-----------------|
| `ModuleNotFoundError: No module named 'yaml'` | Rode `pip install pyyaml` com o ambiente virtual ativo. |
| `gen-erdiagram falhou` ou `FileNotFoundError: 'gen-erdiagram'` | `linkml` não instalado ou venv inativo. Rode `pip install linkml` e `source .venv/bin/activate`. |
| `aviso: Classe.slot sem range de classe; ignorado` | O slot tem `link_type`, mas o `range` não aponta para uma classe do schema. Corrija o `range`. |
| `ValueError: cardinalidade desconhecida` | `cardinalidade` fora de `N:1`, `1:N`, `1:1`, `N:N`. Use aspas no YAML (`"N:1"`). |
| Diagrama não renderiza no GitHub/mermaid.live com `layout: elk` | Alguns renderizadores não suportam ELK. Gere com `--layout dagre`. |

## Auditoria dos contratos documentais

`python3 scripts/validar_contratos_documentais.py`

Confere os schemas propostos de recebimento/ingestão, os exemplos, estados e 14 controles negativos, além da matriz derivada dos 15 casos multimodais. Não extrai documentos nem executa LangGraph ou Langfuse. O validador de schemas local agora também verifica inteiros e valor mínimo, rejeitando booleanos como tamanho/versão.
