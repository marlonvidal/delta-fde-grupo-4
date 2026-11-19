# Amparo Seguros · sinistros pequenos

Certificação FDE · Hotseat Semana 3 · Case 4.

A banca lê primeiro a frase do projeto e os indicadores.

## 1. Em uma frase

Projeto FDE para a Amparo Seguros, seguradora de automóvel com 410.000 apólices, a pedido de Paulo Rezende, vice-presidente de sinistros.

Produto ou serviço escolhido:

## 2. Dor e problema

A seguradora recebe 6.400 avisos de sinistros pequenos por mês (até R$ 5 mil): vidros, retrovisores, para-choques e colisões leves.

Hoje o segurado abre o sinistro no aplicativo e envia fotos; uma oficina manda o orçamento; um analista confere cobertura, fotos e orçamento (cerca de 40 minutos de trabalho); o sinistro espera na fila; o analista aprova dentro da alçada de R$ 5 mil; a oficina ou o segurado recebe. O tempo total médio até o pagamento é de 9,2 dias. Dinheiro pago não volta.

Cada regulação custa R$ 85. Quem espera mais de 7 dias renova menos: 72%, contra 84% de quem recebe em até 7 dias. 62% dos sinistros pequenos passam de 7 dias.

Problema em uma frase (quem, o que acontece, quanto, por quê, quanto custa):

## 3. O que resolve e o que não resolve

Pedido como veio: "Uma IA que aprove e pague sozinha os sinistros pequenos."

Prazo pedido: piloto rodando antes da reunião de diretoria do semestre, em 60 dias.

O que este projeto resolve:

O que fica de fora:

## 4. Indicadores

Números publicados no case. A linha de base adotada, a meta e o valor medido ficam em branco: o case avisa que pelo menos um número engana, e pede para conferir período e forma de cálculo antes de fechar a linha de base.

| Indicador | Número no case | Meta | Medido |
| --- | --- | --- | --- |
| Sinistros pequenos por mês | 6.400 | | |
| Valor médio do sinistro pequeno | R$ 2.300 | | |
| Custo de regulação por sinistro | R$ 85 | | |
| Tempo médio até o pagamento | 9,2 dias | | |
| Sinistros pagos em até 7 dias | 38% | | |
| Sinistros pagos em mais de 7 dias | 62% | | |
| Renovação no ano seguinte, até 7 dias | 84% | | |
| Renovação no ano seguinte, mais de 7 dias | 72% | | |
| Prêmio médio anual | R$ 3.100 | | |
| Fraude na auditoria amostral | 3,1% dos sinistros pequenos | | |
| Vidros | 27% dos sinistros pequenos | | |
| Sinistros até R$ 2 mil, score de fraude baixo e sem outro sinistro em 12 meses | 38% dos pequenos | | |

Métrica norte (resultado que o patrocinador quer ver):

Métrica de entrada (muda antes da norte):

Métrica de proteção (o que não pode piorar):

## 5. Como funciona

Processo atual: aviso → orçamento → regulação → fila → aprovação → pagamento.

| Sistema | O que guarda |
| --- | --- |
| Sistema de sinistros | Avisos, fotos, orçamentos, análises, aprovações e pagamentos com data |
| Score de fraude do fornecedor | Nota de risco de fraude de cada sinistro. Calibrado com sinistros acima de R$ 20 mil |
| Modelo da startup parceira | Classifica tipo e gravidade do dano a partir da foto |

Fluxo da solução (dado de entrada → ação → sistema → quem decide → número):

## 6. Como rodar

Comando:

Diagrama ER da ontologia: `python scripts/gerar_er.py` (setup em `scripts/README.md`).

Dado de exemplo: `data/amostra-sintetica.csv` (cabeçalho apenas). Casos de eval: `src/evals/casos.jsonl` (vazio).

## 7. Falhas conhecidas e limites

Do diagnóstico de dados do case:

- 7% dos sinistros sem nenhuma foto.
- 12% das fotos de segurados com baixa qualidade (escuras, cortadas). O teste do modelo da startup usou 2.000 fotos de oficinas credenciadas e acertou 94% na classificação do dano.
- O score de fraude do fornecedor foi calibrado para sinistros grandes, não para os pequenos.
- O sistema não registra o tempo de trabalho do analista por sinistro.
- Pagamento feito não volta: recuperar valor pago por erro é raro e caro.
- Toda decisão de sinistro pode virar reclamação na ouvidoria e no regulador do setor.

Falhas da solução:

## 8. Handover

Quem opera depois deste projeto:

| Quem | O que faz hoje |
| --- | --- |
| Paulo Rezende, vice-presidente de sinistros | Patrocinador. Responde por custo de regulação, prazo e renovação |
| Analistas de regulação (22) | Analisam e aprovam os sinistros |
| Prevenção a fraude | Audita uma amostra dos sinistros pagos |
| Jurídico e ouvidoria | Respondem por reclamações e pelo regulador do setor |
| Startup parceira | Oferece o modelo que classifica o dano pela foto |

## 9. Equipe

| Entrega | Arquivo | Dono |
| --- | --- | --- |
| 1 · Ontologia | `docs/ontologia/01-ontologia.md` | |
| 2 · Contrato de sucesso | `docs/02-contrato-de-sucesso.md` | |
| 3 · Evals | `src/evals/casos.jsonl` | |
| 4 · Painel de evals | `docs/04-painel-de-evals.md` | |
| 5 · Relatório de impacto | `docs/05-relatorio-de-impacto.md` | |
| 6 · Case | `docs/06-case.pdf` | |
