# Ampliação documental e multimodal — v0.2.0

Rascunho local: **10 novos casos (MMV-006 a MMV-015)**, 39 documentos e 9 imagens recebidas. Somados ao piloto anterior, são 15 casos preparados. Imagens fornecidas por Alex; nenhuma chamada ao agente.

## Cobertura proposta

| Caso | Condição | Rota esperada | Imagem planejada |
|---|---|---|---|
| MMV-006 | Valor exatamente no limite de escopo | ANALISE_COMUM | adequada |
| MMV-007 | Valor um centavo abaixo do limite | ANALISE_COMUM | adequada |
| MMV-008 | Orçamento obrigatório ausente | COMPLEMENTACAO_DOCUMENTAL | adequada |
| MMV-009 | Orçamento explicitamente incompleto | COMPLEMENTACAO_DOCUMENTAL | adequada |
| MMV-010 | Evento após fim da vigência | ANALISE_COMUM | adequada |
| MMV-011 | Evento no primeiro dia de vigência | ANALISE_COMUM | adequada |
| MMV-012 | Única foto fortemente desfocada | COMPLEMENTACAO_DOCUMENTAL | desfocada |
| MMV-013 | Única foto muito escura | COMPLEMENTACAO_DOCUMENTAL | escura |
| MMV-014 | Sinalização humana de suspeita | REVISAO_ESPECIALIZADA | adequada |
| MMV-015 | Conflito de valor e foto ausente | REVISAO_POR_INCERTEZA | ausente |

## Revisão e execução

1. Revisar documentos, regras simuladas e gabaritos em `revisao.html`. Confirmar especialmente evento fora da vigência na fila comum com recomendação de revisão humana, e precedência de incerteza sobre complementação.
2. As nove imagens já foram recebidas. Não confundir alvo do prompt com rótulo confirmado.
3. Conferir cada imagem e revisar o gabarito correspondente. Registrar revisão humana antes de usar como referência validada.
4. Rodar `python3 scripts/validar_ampliacao_multimodal.py`. O comando padrão valida preparação; `--pronto` exige imagens e revisão aprovadas e bloqueia este rascunho.
5. Importação autorizada por Alex e conferida pela API. Manter `input`, `expectedOutput` e `metadata` separados. O input continua no formato do piloto. O gabarito usa critérios parciais por módulo e precisa de alinhamento com a saída de Samuel.

## Uso dos dados

Todos os casos são de desenvolvimento, da família de variações FDE-001. Não distribuir pares quase iguais entre desenvolvimento e teste: isso inflaria os resultados. Casos de avaliação reservada deverão usar novas combinações e materiais independentes e revisão humana. O volume não permite inferir desempenho operacional ou as taxas de fotos ruins/ausentes da reunião.

Somente `input` segue para o agente. Títulos, prompts, alvo visual, resultado esperado e página de revisão são materiais do avaliador. Caminhos locais de imagem precisam ser resolvidos pelo executor para bytes; falta do arquivo previsto bloqueia a execução. Em MMV-015 o inventário vazio é ausência intencional no caso.

## Identificadores

O prefixo MMV distingue este lote do catálogo anterior FDE-006 a FDE-030, que contém outros cenários. A família de origem FDE-001 identifica o template usado, não equivalência entre os casos.

## Recebimento das imagens

Nove PNGs copiados de Downloads, com originais preservados. Corrigidos os nomes com ponto extra (MMV-007) e extensão duplicada (MMV-010). Hashes registrados. Inspeção do assistente identificou sete fotos com trincas visíveis, uma fortemente desfocada e uma muito escura. Revisão humana dos rótulos continua pendente. Lote importado no Langfuse; revisão humana dos gabaritos pendente.

## Estado atual no Langfuse

Importação conferida pela API: 10 casos. Dataset: [amparo-ampliacao-multimodal-v0](https://us.cloud.langfuse.com/project/cmwtuztw500wjad0d8k6znpmu/datasets/cmwtzx5gf03ewad0jsmxbeqd9). Identificadores de condições padronizados para `CONDICOES` e tipo `condicoes`. Gabaritos continuam pendentes de revisão humana; nenhum experimento do agente foi executado.
