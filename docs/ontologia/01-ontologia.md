# Ontologia

Entrega 1. Fonte: seção 5 do case (`docs/06-case.pdf`), relatório de diagnóstico de dados no formato do CRISP-DM, organizado nos cinco blocos. Descreve o que existe e o que falta. Não escolhe solução.

## Termos

| Termo | O que significa |
| --- | --- |
| Sinistro | Evento coberto pelo seguro, como uma batida ou um vidro quebrado, que gera o pedido de indenização |
| Regulação | Análise do sinistro: confere cobertura, fotos, orçamento e decide se paga e quanto |
| Fraude em sinistro | Pedido de indenização por dano falso, aumentado ou anterior à apólice |
| Renovação | O segurado contrata o seguro de novo no ano seguinte |

## Fontes

| Fonte | Conteúdo | Dono |
| --- | --- | --- |
| Sistema de sinistros | Avisos, fotos, orçamentos, decisões, pagamentos | Sinistros |
| Histórico de apólices | 5 anos de apólices e sinistros por CPF | TI |
| Auditoria de fraude | Amostra mensal de sinistros pagos | Prevenção a fraude |

## Peças (objetos e identidade)

Existe: apólice, veículo, segurado, sinistro e oficina, cada um com identificador único.

Falta ou tem problema: 7% dos sinistros sem foto.

## Tabuleiro (relações)

Existe: sinistro ligado à apólice e ao histórico do CPF há 5 anos.

Falta ou tem problema: nenhuma falta relevante.

## Regras

Existe: cobertura escrita nas condições gerais; alçada do analista de até R$ 5 mil.

Falta ou tem problema: score de fraude calibrado para sinistros grandes, não para os pequenos.

## Jogadas (estados e eventos)

Existe: todas as etapas com data e hora (aviso, orçamento, regulação, fila, aprovação, pagamento).

Falta ou tem problema: não registra o tempo de trabalho do analista por sinistro.

## Conferir a caixa (qualidade)

Existe: orçamentos completos em 100%.

Falta ou tem problema: 12% das fotos de segurados com baixa qualidade.

## Diagrama ER

- Schema (fonte): [`amparo_core.yaml`](amparo_core.yaml)
- Diagrama: [`er.pdf`](er.pdf), gerado a partir de [`er.mmd`](er.mmd)
- Como regenerar: [`scripts/README.md`](../../scripts/README.md)

## Restrições

- Pagamento feito não volta: recuperar valor pago por erro é raro e caro.
- Toda decisão de sinistro pode virar reclamação na ouvidoria e no regulador do setor.
- Piloto esperado em 60 dias.
