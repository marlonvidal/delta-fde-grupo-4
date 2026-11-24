# Catálogo técnico dos 15 casos documentais

24/11/2026 · Matriz de rastreabilidade derivada dos lotes locais, com status MMV aceitos por Alex em 24/11/2026 e incorporados aos gabaritos 0.2.2. A revisão visual/documental foi concluída por Alex e sincronizada no Langfuse.

| Caso | Condição | Documentação | Rota | Recomendação no fluxo | Módulos executados |
|---|---|---|---|---|---|
| FDE-001 | Documentos completos e foto adequada | COMPLETA | ANALISE_COMUM | RECOMENDAR_APROVACAO | documentacao, triagem, parecer, recomendacao |
| FDE-002 | Foto ausente | PENDENTE | COMPLEMENTACAO_DOCUMENTAL | Não executada | documentacao, triagem |
| FDE-003 | Aviso 2300.00; orçamento 1800.00 | INDETERMINADA | REVISAO_POR_INCERTEZA | Não executada | documentacao, triagem |
| FDE-004 | Condições de cobertura ausentes | COMPLETA | REVISAO_POR_INCERTEZA | Não executada | documentacao, triagem |
| FDE-005 | Valor 5000.01 | Não avaliada | FORA_ESCOPO | Não executada | documentacao, triagem |
| MMV-006 | Valor 5000.00, inclusivo | COMPLETA | ANALISE_COMUM | RECOMENDAR_APROVACAO | documentacao, triagem, parecer, recomendacao |
| MMV-007 | Valor 4999.99 | COMPLETA | ANALISE_COMUM | RECOMENDAR_APROVACAO | documentacao, triagem, parecer, recomendacao |
| MMV-008 | Orçamento ausente | PENDENTE | COMPLEMENTACAO_DOCUMENTAL | Não executada | documentacao, triagem |
| MMV-009 | Orçamento incompleto | PENDENTE | COMPLEMENTACAO_DOCUMENTAL | Não executada | documentacao, triagem |
| MMV-010 | Evento após fim de vigência | PENDENTE | ANALISE_COMUM | REVISAO_HUMANA | documentacao, triagem, parecer, recomendacao |
| MMV-011 | Evento no primeiro dia da vigência | COMPLETA | ANALISE_COMUM | RECOMENDAR_APROVACAO | documentacao, triagem, parecer, recomendacao |
| MMV-012 | Foto desfocada | PENDENTE | COMPLEMENTACAO_DOCUMENTAL | Não executada | documentacao, triagem |
| MMV-013 | Foto subexposta | PENDENTE | COMPLEMENTACAO_DOCUMENTAL | Não executada | documentacao, triagem |
| MMV-014 | Sinalização humana de suspeita | COMPLETA | REVISAO_ESPECIALIZADA | Não executada | documentacao, triagem |
| MMV-015 | Conflito de valor e foto ausente | PENDENTE | REVISAO_POR_INCERTEZA | Não executada | documentacao, triagem |

## Status por módulo

| Caso | Documentação | Triagem | Parecer | Recomendação | Origem |
|---|---|---|---|---|---|
| FDE-001 | CONCLUIDO | CONCLUIDO | CONCLUIDO | CONCLUIDO | Gabarito existente |
| FDE-002 | CONCLUIDO | CONCLUIDO | NÃO EXECUTADO | NÃO EXECUTADO | Gabarito existente |
| FDE-003 | INSUFICIENTE | INSUFICIENTE | NÃO EXECUTADO | NÃO EXECUTADO | Gabarito existente |
| FDE-004 | CONCLUIDO | INSUFICIENTE | NÃO EXECUTADO | NÃO EXECUTADO | Gabarito existente |
| FDE-005 | FORA_ESCOPO | FORA_ESCOPO | NÃO EXECUTADO | NÃO EXECUTADO | Gabarito existente |
| MMV-006 | CONCLUIDO | CONCLUIDO | CONCLUIDO | CONCLUIDO | Aceito por Alex · 24/11/2026 |
| MMV-007 | CONCLUIDO | CONCLUIDO | CONCLUIDO | CONCLUIDO | Aceito por Alex · 24/11/2026 |
| MMV-008 | CONCLUIDO | CONCLUIDO | NÃO EXECUTADO | NÃO EXECUTADO | Aceito por Alex · 24/11/2026 |
| MMV-009 | CONCLUIDO | CONCLUIDO | NÃO EXECUTADO | NÃO EXECUTADO | Aceito por Alex · 24/11/2026 |
| MMV-010 | CONCLUIDO | CONCLUIDO | CONCLUIDO | CONCLUIDO | Aceito por Alex · 24/11/2026 |
| MMV-011 | CONCLUIDO | CONCLUIDO | CONCLUIDO | CONCLUIDO | Aceito por Alex · 24/11/2026 |
| MMV-012 | CONCLUIDO | CONCLUIDO | NÃO EXECUTADO | NÃO EXECUTADO | Aceito por Alex · 24/11/2026 |
| MMV-013 | CONCLUIDO | CONCLUIDO | NÃO EXECUTADO | NÃO EXECUTADO | Aceito por Alex · 24/11/2026 |
| MMV-014 | CONCLUIDO | CONCLUIDO | NÃO EXECUTADO | NÃO EXECUTADO | Aceito por Alex · 24/11/2026 |
| MMV-015 | INSUFICIENTE | INSUFICIENTE | NÃO EXECUTADO | NÃO EXECUTADO | Aceito por Alex · 24/11/2026 |

## Semântica de execução

- FDE-002 a FDE-005 guardam expectativas dos quatro módulos para testes individuais. No fluxo integrado só os módulos da coluna executados são chamados. Os demais critérios não autorizam produzir parecer ou recomendação fictícios.
- Em MMV-015, foto ausente é pendência confirmada e o conflito de valor mantém a análise documental incompleta: documentação `PENDENTE` com `INSUFICIENTE`; triagem por incerteza com `INSUFICIENTE`. Status e revisão visual/documental aceitos por Alex em momentos separados.
- MMV-010 explicita cobertura contradita pela vigência, documentação pendente e recomendação humana no ramo comum. Essa rota segue o gabarito existente; não foi reclassificada. Decisão 2A confirmada por Samuel, com concordância de Breno: MMV-010 e os antigos FDE-017/FDE-018 usam esse mesmo tratamento.
- Nenhum caso demonstra retorno do especialista, falha de leitura ou ingestão de arquivo corrompido. As 12 variantes de formato referem-se apenas a FDE-001 e FDE-003; não são 12 novos cenários de negócio nem testes reservados.
- A referência estruturada inclui vínculos de documentos, imagens, regras e origem: [rastreabilidade-15-casos.json](../../src/evals/ingestao/rastreabilidade-15-casos.json).

## Aceite visual e documental — 24/11/2026

Alex confirmou a inadequação de MMV-012 por desfoque e MMV-013 por subexposição, e confirmou dano no vidro visível e documentos coerentes nos casos de foto adequada. Revisão registrada por Alex, sem revisão independente ou execução do agente. Esta atualização encerra a pendência local de revisão visual; aceite sincronizado no Langfuse e conferido pela API em 24/11/2026.
