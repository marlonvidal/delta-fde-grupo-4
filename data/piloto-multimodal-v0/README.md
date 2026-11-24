# Piloto documental e multimodal

Cinco casos de desenvolvimento (FDE-001 a FDE-005), 19 documentos TXT e quatro imagens PNG. Gabarito 0.1.1: revisão visual/documental de Alex concluída em 24/11/2026 e sincronizada no Langfuse. Não são os cinco casos reais mencionados na reunião nem resultados do agente.

| Caso | Condição | Rota |
|---|---|---|
| FDE-001 | Documentos consistentes e foto adequada | ANALISE_COMUM |
| FDE-002 | Foto ausente | COMPLEMENTACAO_DOCUMENTAL |
| FDE-003 | Aviso 2300.00 e orçamento 1800.00 | REVISAO_POR_INCERTEZA |
| FDE-004 | Condições de cobertura ausentes | REVISAO_POR_INCERTEZA |
| FDE-005 | Valor 5000.01 | FORA_ESCOPO |

## Estrutura e execução

- `entradas.jsonl` e `entradas/`: somente `input` segue para o agente. Metadados, gabaritos e prompts não são entradas de execução.
- `documentos/` e seu manifesto: textos e hashes vinculados ao caso. São TXT, não documentos para OCR.
- `imagens/` e seu manifesto: bytes reais, hashes e revisão de Alex. A ausência de FDE-002 é intencional.
- `avaliador/verdade.jsonl`: critérios parciais individuais e fluxo esperado; não equivale a resposta completa gerada.
- `prompts/`: origem da preparação visual, restrita ao avaliador; rótulos dependem da imagem revisada, não do prompt.

No fluxo integrado, apenas FDE-001 chama os quatro módulos. As outras rotas encerram a passagem após documentação e triagem. Os critérios individuais de parecer/recomendação não autorizam fabricar respostas dos módulos pulados.

`R-COB` deriva do documento de condições quando fornecido. Não está em `input.regras`, nem pode ser injetada em FDE-004. O [contrato de ingestão](../../docs/contratos/06-chat-ingestao-documental.md) descreve a normalização/proveniência necessária para integrar os schemas de saída. Referências locais de imagens precisam ser resolvidas para bytes pelo executor.

## Validação e limites

`python3 scripts/validar_piloto_multimodal.py`

O comando confere estrutura, vínculos e hashes. Não executa visão, OCR ou agente. A revisão foi realizada por Alex, sem revisão independente. O lote não representa prevalência operacional; classificação visual não pode inferir fraude, valor de reparo ou cobertura isoladamente. As regras são do exercício.

## Langfuse

[amparo-piloto-multimodal-v0](https://us.cloud.langfuse.com/project/cmwtuztw500wjad0d8k6znpmu/datasets/cmwtwu27x01zgad0jyzn7uyfg). Critérios e aceite conferidos pela API; estado e data da sincronização no `manifesto.json`.
