# Dataset inicial de avaliações

Versão 0.3.1 · 24/11/2026 · **Cenários aprovados por Alex em 20/11/2026**.

O lote tem 30 cenários sintéticos de desenvolvimento e quatro expectativas por cenário. Não é conjunto reservado, não deriva de falhas observadas e não contém resultados de agentes. Não substitui a exigência final de casos vindos de falhas observadas.

## Arquivos

- `caso.schema.json`: JSON Schema Draft 2020-12 para o envelope do dataset; dados de domínio e expectativas específicas são parcialmente abertos nesta versão.
- `casos.jsonl`: um objeto JSON por linha, autossuficiente.
- `../../scripts/validar_dataset.py`: verificação local do subconjunto de JSON Schema utilizado e invariantes das 30 fixtures, usando biblioteca padrão. Não é validador genérico de JSON Schema nem validação LinkML.

Execute na raiz:

```sh
python3 scripts/validar_dataset.py
```

## Como executar sem revelar o resultado

Para cada linha, enviar **somente `entrada`** ao módulo. `esperado`, título, tags, justificativa e metadados ficam no avaliador. Executar os módulos separadamente sobre a mesma entrada. Não fornecer decisão final nem dados posteriores à análise.

`esperado` contém **asserções parciais**, não respostas completas para copiar: comparar `status_execucao` e cada campo de `campos_iguais` com a saída, além de conferir todo o contrato de saída do módulo. Arrays de motivos são conjuntos sem ordem. Textos livres não exigem igualdade literal: revisar pelas `checagens_humanas` e pela rubrica dos contratos. `falhas_criticas` complementa as falhas definidas nos contratos; não é uma lista exaustiva.

Referências de evidências e regras presentes na resposta devem existir na entrada. O agente deve produzir o restante dos campos obrigatórios do contrato mesmo que não haja asserção exata para cada um. `caso.schema.json` valida o caso de teste, não a saída do agente.

Veja o [catálogo completo dos 30 cenários](catalogo.md). A tabela abaixo resume os cinco cenários iniciais.

## Cenários e expectativas resumidas

| ID | Cenário | Documentação | Triagem | Parecer: cobertura | Recomendação |
|---|---|---|---|---|---|
| FDE-001 | Completo | Completa | Análise comum | Sustentada pelas regras simuladas | Recomendar aprovação de elegibilidade, sem valor e sem executar |
| FDE-002 | Sem foto | Pendente | Complementação | Sustentada; documentação pendente | Revisão humana |
| FDE-003 | Valores conflitantes | Indeterminada | Revisão por incerteza | Sustentada, mas parecer parcial com conflito | Revisão humana |
| FDE-004 | Cobertura indisponível | Completa | Revisão por incerteza | Não verificável | Revisão humana |
| FDE-005 | R$ 5.000,01 | Fora do escopo | Fora do escopo | Sem conclusão | Revisão humana, fora do escopo |

FDE-005 é um teste de fronteira no envelope de avaliação; propositalmente excede o limite da classe Sinistro no LinkML. As fixtures não são instâncias completas do container LinkML.

## Regras e dados sintéticos

Todas as regras são `SIMULADA`, inclusive regras de cobertura, obrigatoriedade documental e filas. O limite de R$ 5.000 é inspirado no case, mas sua aplicação uniforme aos quatro módulos é proposta do teste. Não há recomendação de valor de indenização; o cálculo é humano.

Em FDE-004, a regra R-COB não é entregue: o catálogo de cobertura é explicitamente parcial. Em FDE-003, a cobertura sintética depende de tipo de dano e vigência, não do valor exato; por isso pode estar sustentada enquanto o parecer permanece insuficiente para uma conclusão financeira.

Dinheiro é string decimal BRL, por exemplo `"1800.00"`; o executor usa Decimal. `data_evento` e a sinalização humana de suspeita estão em `contexto_avaliacao`, extensão do envelope, não novos campos confirmados da ontologia. A sinalização indica suspeita informada, não fraude comprovada. Somente metadados de foto são usados; não há arquivos de imagem. Ausência de histórico é `null`, não `false`.

## Revisão antes de ampliar

- [ ] Samuel confirma interface e saídas dos módulos.
- [ ] Breno e grupo revisam mapeamento e regras simuladas.
- [ ] Alex e revisor independente validam os rótulos e rubricas.
- [x] Acrescentar gatilho especializado, qualidade de foto, valores no limite e ataques por instruções em documentos.
- [x] Ampliar a base para 30 casos, todos de desenvolvimento; nenhum foi declarado reservado.
- [ ] Definir esquema específico de respostas e executor antes de medir os agentes.

Nenhuma taxa de acerto, economia ou impacto foi medida neste lote.

## Histórico: versão 0.2.0 (substituída pela 0.3.0)

Mais 25 cenários, totalizando 120 expectativas parciais. Regras artificiais esclarecem limites inclusivos de vigência, tratamento de campos desconhecidos, precedência de triagem e necessidade de cálculo para recomendar valor. Contratos de comportamento permanecem na versão 0.1.0, ainda propostos. As extensões de contexto e o texto não confiável do orçamento são fixtures do envelope, não campos confirmados por Breno. A base é pequena e orientada à cobertura; frequências de classes não estimam a operação.

## Registro de aprovação

Os 30 cenários foram revisados e aprovados por Alex em 20/11/2026. Status: `APROVADO_POR_ALEX`. As regras permanecem simuladas. A aprovação é dos comportamentos esperados; não comprova desempenho de agente nem valida condições reais de seguro. Alterações de saída estão registradas na versão 0.3.0 abaixo.

## Versão 0.3.0 — decisões de saída de Alex

Contratos 0.2.0; schemas de saída em `schemas/saidas/` e 20 respostas de referência em `exemplos-saida/`. Veja o [guia de integração](../../docs/guia-integracao-avaliacoes.md). Sem negativa nem valor sugerido, com evidências por conclusão e próxima ação humana para impedimentos. Removida R-VAL. FDE-030 espera aprovação de elegibilidade se demais critérios atendidos; todos os demais rótulos permanecem. Os exemplos de resposta foram sincronizados. Nenhum exemplo foi gerado por execução de agente.

## Versão 0.3.1 — vigência

FDE-017 e FDE-018 seguem `ANALISE_COMUM`, com parecer de cobertura contradita e recomendação `REVISAO_HUMANA`, conforme decisão 2A confirmada em 24/11/2026. Demais fatos e expectativas foram preservados. Schemas de saída continuam 0.2.0 e regras preservam suas versões próprias; a revisão é do dataset.
