# Ampliação documental e multimodal

Dez casos de desenvolvimento (MMV-006 a MMV-015), 39 documentos TXT e nove imagens PNG. Gabarito 0.2.2: status por módulo e revisão visual/documental aceitos por Alex e sincronizados no Langfuse em 24/11/2026. Nenhum agente foi executado.

## Cobertura

| Caso | Condição | Rota esperada | Evidência visual revisada |
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


## Regras e execução

Evento fora da vigência (MMV-010) mantém análise comum, parecer apontando cobertura contradita e recomendação de revisão humana, sem negativa. Após especialista (MMV-014), o parecer volta ao analista; não há retomada automática do agente. Em MMV-015, o conflito de valor tem precedência sobre a foto ausente, que permanece como pendência secundária.

Alex confirmou a inadequação de MMV-012 por desfoque e MMV-013 por subexposição. As demais fotos mostram dano em vidro com qualidade adequada; documentos foram considerados coerentes com os cenários. Ausência de foto em MMV-015 é intencional. Revisão de Alex não equivale a revisão independente ou resultado do agente.

Somente `input` segue para o agente. `avaliador/verdade.jsonl` contém critérios parciais e a seleção dos módulos do fluxo; não é uma resposta completa produzida. Prompts, títulos e rótulos são restritos ao avaliador. Caminhos de imagens precisam ser resolvidos para bytes; falha de acesso não é ausência de foto do segurado. A integração depende de extração/normalização conforme o [contrato de ingestão](../../docs/contratos/06-chat-ingestao-documental.md).

## Validação

`python3 scripts/validar_ampliacao_multimodal.py --pronto`

Verifica arquivos, hashes, vínculos, critérios e registro de revisão. O estado pronto significa fixtures disponíveis, não suporte implementado no agente.

## Uso e identificadores

Todos os casos derivam da mesma família de desenvolvimento. Não separar variantes quase idênticas entre desenvolvimento e avaliação reservada. O prefixo MMV distingue esses cenários dos antigos FDE-006 a FDE-030, que têm outros significados. O volume não representa taxas operacionais de foto ruim/ausente ou desempenho real.

## Langfuse

[amparo-ampliacao-multimodal-v0](https://us.cloud.langfuse.com/project/cmwtuztw500wjad0d8k6znpmu/datasets/cmwtzx5gf03ewad0jsmxbeqd9). Critérios e aceite conferidos pela API; estado e datas no `manifesto.json`.
