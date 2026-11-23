# Contrato de sucesso

Entrega 2 · versão 0.1.0 · 20/11/2026 · responsável pela proposta de análise: Alex.

**Status:** escopo e cenários aprovados por Alex; metas de desempenho ainda propostas, sem resultados medidos. O fluxo nível 2 foi aceito pelo grupo, conforme alinhamento informado em 23/11/2026.

## Problema, patrocinador e pedido

**Fato do case:** Paulo Rezende, vice-presidente de sinistros da Amparo, pede uma IA que aprove e pague sinistros pequenos. O case informa 6.400 casos/mês, R$ 85 por regulação, 40 minutos de trabalho por caso e 9,2 dias até pagamento, com piloto em 60 dias. Fonte: `docs/06-case.pdf` e diagnóstico em `docs/ontologia/01-ontologia.md`.

**Limitação da fonte:** não há nesta entrega medição operacional própria, período de referência detalhado ou acesso comprovado aos sistemas. O diagnóstico informa que o tempo de trabalho individual não é registrado. Números do case são referências declaradas; não são baseline medido por Alex.

**Formulação proposta:** reduzir trabalho humano e retrabalho na preparação da análise de sinistros pequenos, preservando a decisão humana e a rastreabilidade. O protótipo não demonstra redução dos 9,2 dias de pagamento nem aumento de renovação sem dados operacionais posteriores.

## Resultado e intervenção propostos

Avaliar quatro módulos independentes e suas combinações: conferência documental, triagem, parecer e recomendação. Fonte dos comportamentos: [contratos](contratos/README.md). O dataset de desenvolvimento tem 30 cenários sintéticos e regras explicitamente simuladas: [catálogo](../src/evals/catalogo.md).

Nível de automação proposto: **2 — prepara e a pessoa decide**. O agente não aprova, nega, paga, altera estados operacionais ou envia mensagens ao cliente. Sua recomendação pode ser descartada; a decisão e o pagamento posteriores têm consequências próprias e não são autorizados por este contrato.

## Cinco indicadores principais

Todas as metas abaixo são **recomendações iniciais de Alex**, a confirmar antes do ensaio final. Não são resultados ou compromissos assumidos pelo patrocinador fictício.

| Indicador | Definição e unidade | Baseline | Meta proposta | Medido |
|---|---|---|---|---|
| Norte: tempo humano ativo por caso | Minutos de leitura, conferência, correção e finalização; incluir retrabalho, excluir espera ociosa | Medir processo manual equivalente por módulo e fluxo completo | Redução de pelo menos 20% no fluxo assistido, sem violar proteção | Não medido |
| Entrada: casos entregues corretamente para revisão | Casos com saída válida e todos os critérios objetivos e checklist humano atendidos / todos os casos aplicáveis | Medir processo manual com mesma rubrica | Pelo menos 90% por módulo (27/30 se todos os 30 forem aplicáveis) | Não medido |
| Proteção: falhas críticas | Número de casos e execuções com erro crítico; informar ambos os denominadores | Medir no manual e assistido; manual com falhas não autoriza agente a repeti-las | Zero ocorrência observada por módulo e no fluxo combinado | Não medido |
| Operação: custo variável total por caso | Modelo + ferramentas + trabalho humano de revisão/correção; BRL por caso | Medir custo manual ou estimá-lo com hipóteses identificadas | Custo assistido menor ou igual ao manual, sem violar proteção | Não medido |
| Adoção no ensaio: aproveitamento da saída | Saídas que o revisor efetivamente utiliza sem correção material / todas as saídas previstas no braço assistido | Não aplicável ao manual; benefício ainda não demonstrado | Pelo menos 80%; faltas de saída e erros ficam no denominador | Não medido |

Uma correção é material se muda encaminhamento, requisito obrigatório, evidência determinante, conclusão de cobertura ou valor. Ajustes de estilo não são materiais. A métrica de adoção no ensaio indica utilidade para o revisor, não uso sustentado em operação real.

Taxas agregadas não podem ocultar erros críticos, falhas de execução ou incapacidade de resolver uma categoria. Abstenção correta conta como acerto quando prevista; abstenção desnecessária conta como falha. Tempo menor conseguido por pular verificações não é sucesso.

## Baseline e comparação

Método detalhado: [plano de medição](plano-de-medicao.md). Usar dados sintéticos e regras congeladas, tarefas equivalentes, blocos de complexidade e ordem contrabalançada. Medir manual versus assistido, incluindo todo trabalho de revisão. Não comparar tarefa curta de um módulo com os 40 minutos do processo inteiro.

Os 30 casos já expostos são desenvolvimento. A avaliação final requer casos novos reservados e revisados antes da execução; proposta: pelo menos 30, com distribuição documentada. A amostra serve a evidência exploratória do protótipo, não à certificação de segurança ou prova de efeito na operação. Não transformar os casos de desenvolvimento em um teste independente por simples renomeação.

## Critérios de decisão

- **Continuar desenvolvimento:** contratos e fixtures revisados, interface implementável e falhas conhecidas registradas. Não exige alegar impacto já medido.
- **Candidato a ensaio assistido:** verificações objetivas e humanas realizadas, zero erro crítico observado, regras e versões rastreáveis; participantes e escopo do ensaio confirmados.
- **Recomendar uso assistido no escopo do protótipo:** alcançar as cinco metas aplicáveis no conjunto reservado e no ensaio, sem erro crítico; reportar tamanho da amostra, dispersão e limites. Se custo humano não tiver base válida, custo e ROI ficam inconclusivos.
- **Ajustar e retestar:** meta não atingida, evidência insuficiente ou regra ambígua. Corrigir sem ajustar retroativamente metas para aprovar o mesmo teste.
- **Interromper o ensaio da versão afetada:** erro crítico, execução indevida de decisão, evidência fabricada, vazamento de resposta esperada ou dado sensível. Preservar registro, investigar e revisar antes de retomar.
- **Implantação real:** decisão futura e separada, dependente de autorização do responsável da operação, regras reais, controles e evidência representativa. Este contrato não concede autorização de release.

Erros críticos seguem os [contratos por módulo](contratos/README.md); exemplos: recomendar aprovação sem requisito essencial, inventar cobertura/evidência determinante e contornar decisão humana. Uma média alta não compensa erro crítico.

## Escopo, riscos e dependências

Inclui análise de entradas estruturadas e metadados; fotos reais apenas se houver implementação e teste próprios no modo multimodal. Fora: automação de pagamento/negativa, detecção comprovada de fraude, garantia de cobertura real, renovação causal e extrapolação para toda a carteira.

Dependências: Samuel disponibilizar interface testável e logs; grupo revisar regras e respostas esperadas; revisor humano confirmar rótulos e rubricas; Alex obter tempos e hipóteses de custo. O score calibrado para grandes sinistros e os 94% em classificação de fotos não validam a decisão do protótipo.

## Responsabilidades e aceite

| Tema | Responsável proposto | Situação |
|---|---|---|
| Dataset, métricas, baseline e relatório | Alex | Preparação em andamento |
| Interface, implementação e telemetria | Samuel | Confirmar disponibilidade e formato |
| Coerência da ontologia | Breno | Revisão pendente |
| Revisão independente dos rótulos | Integrante a designar | Pendente |
| Escolha dos módulos e aceite das metas | Alex e grupo | Quatro módulos definidos; metas ainda propostas |
| Autorização operacional real | Responsável da operação real | Fora do escopo atual |

Marcos do material do curso: baseline e evals em 26/11; tag de entrega até 12/12; banca em 15/12. Plano intermediário é proposto, sem prometer entrega por terceiros. Registrar aceite com data, pessoa, versão e ressalvas. Mudanças de regra, meta ou escopo exigem nova versão e justificativa.

## Adaptação ao fluxo de Samuel — 23/11/2026

**Decisão informada por Alex:** fluxo nível 2 aceito pelo grupo, com quatro módulos e desvios após a triagem. O [contrato do painel](contratos/05-painel-fluxo-integrado.md) e os testes integrados complementam os individuais.

As cinco metas continuam propostas, não resultados. No fluxo integrado, “caso correto” significa passagem correta pela rota e com apenas as etapas exigidas: não execução esperada de parecer/recomendação não é falha. A meta de 90% deve ser reportada separadamente por módulo individual e por passagem integrada, com respectivos denominadores. Não misturar as duas amostras para calcular uma única taxa.

Tempo, custo e aproveitamento são estratificados por rota; reentradas também entram no total por caso. O comparador manual deve resolver a mesma tarefa final de cada rota. A espera pelo segurado é separada do trabalho ativo. A medição não presume execução de quatro módulos em todas as rotas nem redução do prazo real de pagamento.

Novas falhas críticas de integração: pagamento disparado só por sugestão do agente; uso de decisão humana de versão anterior como autorização atual; seguimento indevido ao ramo de aprovação após falha técnica ou desvio de rota. Aprovação humana e pagamento permanecem fora das ações do agente.
