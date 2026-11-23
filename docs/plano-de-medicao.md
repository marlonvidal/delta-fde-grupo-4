# Plano de medição — Alex

Versão 0.1.0 · 20/11/2026 · **proposta sem resultados medidos**.

## O que preparar antes do agente

- [ ] Revisar [contratos](contratos/README.md), regras simuladas e rótulos do dataset com revisor designado.
- [ ] Fechar quais módulos e combinações serão construídos; cada comparação mantém a mesma tarefa nos braços manual e assistido.
- [ ] Confirmar os cinco indicadores e metas do [contrato de sucesso](02-contrato-de-sucesso.md).
- [ ] Registrar a versão congelada de regras, casos, instruções e critérios de erro.
- [ ] Preparar casos novos reservados; não usar resultados desses casos para ajustar o agente antes da avaliação final.
- [ ] Definir o custo-hora humano documentado ou cenários de sensibilidade claramente hipotéticos.
- [ ] Ensaiar a coleta manual com casos de desenvolvimento; registrar dificuldades sem inventar observações.

## Coleta manual e ensaio assistido

1. Treinar o avaliador com os casos de desenvolvimento. Fornecer apenas entrada e regras; os rótulos ficam com o revisor da avaliação.
2. Definir unidade: um caso/módulo ou um caso/fluxo completo. Não somar tempos sobrepostos entre módulos nem economias de tarefas compartilhadas.
3. Usar pares de cenários equivalentes por complexidade, com variantes inéditas, para evitar que a mesma pessoa simplesmente lembre a resposta. Alternar ordem manual/assistido entre blocos; preferir revisores diferentes quando viável. Registrar IDs dos pares, revisores e ordem.
4. Medir tempo ativo do início da leitura até finalizar a tarefa, com pausas excluídas e retrabalho incluído. Registrar espera/latência separadamente. Falha de execução não exclui o caso: incluir o tempo gasto e o trabalho manual de recuperação.
5. Avaliar ambas as condições pela mesma rubrica e por revisor que não receba a condição, quando isso for viável. Registrar quando o cegamento for impossível e qualquer efeito de aprendizagem.
6. Guardar rótulos, respostas e notas separadamente da entrada do agente. Registrar divergências entre revisores e resolução fundamentada.
7. Comparar média e mediana de tempo, dispersão (mínimo, máximo e percentis quando a amostra permitir) e resultados por categoria. Não anunciar causalidade em operação real a partir deste ensaio.

Proposta de amostra final: pelo menos 30 cenários reservados e revisados, com grupos de complexidade e casos críticos explícitos; cada módulo deve informar quantos se aplicam. O grupo pode ampliar a amostra ou classificar evidência como insuficiente. Não calcular intervalo de confiança tratando repetições do mesmo cenário como pessoas/casos independentes.

## Fórmulas

- `reducao_tempo = (media_manual - media_assistida) / media_manual`, se média manual > 0 e tarefas comparáveis.
- `custo_humano = minutos_ativos / 60 × custo_hora_BRL`.
- `custo_modelo = tokens_entrada × preco_entrada_por_milhao / 1_000_000 + tokens_saida × preco_saida_por_milhao / 1_000_000`, ajustando cache e outros componentes cobrados conforme uso real.
- `custo_assistido = custo_humano + custo_modelo + custo_ferramentas_variavel`; registrar tentativas repetidas e chamadas de todos os módulos usados.
- `economia_unitaria_estimada = custo_manual - custo_assistido`. Trabalho liberado não é automaticamente redução de gasto de pessoal.
- `beneficio_mensal_estimado = volume_elegivel_adotado × economia_unitaria_estimada - custos_fixos_incrementais`.
- `ROI_no_periodo = (beneficios_monetarios_realizaveis - custos_incrementais_totais) / custos_incrementais_totais`, somente com denominador > 0, mesmo período e custos sem dupla contagem. Benefício não deve já estar líquido dos mesmos custos subtraídos outra vez.

Não multiplicar automaticamente a economia pela totalidade dos 6.400 sinistros do case. Volume elegível, adesão, composição das tarefas e capacidade realizável precisam de justificativa. Renovação e prêmio não são lucro nem impacto causal demonstrado. Preços atuais de modelos serão consultados quando o modelo for escolhido; nenhum preço foi presumido aqui.

## Registro por execução

Usar [modelo de coleta](../data/medicoes-template.csv), inicialmente só com cabeçalho. Uma linha representa uma execução de um braço. Identificadores não contêm dados pessoais de clientes.

| Campo | Definição |
|---|---|
| `experimento_id`, `execucao_id`, `par_id` | IDs do estudo, execução e pareamento |
| `caso_id`, `particao`, `modulo_ou_fluxo` | Caso, desenvolvimento/reservado e unidade medida |
| `condicao`, `ordem`, `revisor_id` | MANUAL/ASSISTIDO, ordem no bloco e revisor pseudônimo |
| `versao_dataset`, `versao_regras`, `versao_agente`, `modelo` | Proveniência; campos de agente vazios no braço manual |
| `inicio`, `fim`, `pausa_min`, `tempo_ativo_min`, `retrabalho_min`, `latencia_s` | Datas com fuso e tempos; retrabalho já incluído no ativo, não somar novamente |
| `saida_valida`, `criterios_atendidos`, `erro_critico`, `saida_utilizada`, `correcao_material` | Booleanos true/false; desconhecidos vazios, nunca tratados como false |
| `status_execucao`, `motivo_falha` | Resultado, abstenção ou erro; preservar registros malsucedidos |
| `tokens_entrada`, `tokens_saida`, `custo_modelo_brl`, `custo_ferramentas_brl` | Consumo real; vazio quando indisponível, não zero presumido |
| `custo_hora_brl`, `origem_custo_hora`, `custo_total_brl` | Base real ou hipótese identificada; total só com componentes disponíveis |
| `referencia_evidencia`, `observacoes` | Caminho do registro e limitações, sem segredos |

## Diagnósticos específicos

Documentação: precisão e recall por requisito obrigatório; distinguir desconhecido de ausência. Triagem: matriz multiclasse e recall de revisão especializada. Parecer: notas 0–2 por dimensão e alegações sem suporte. Recomendação: falso positivo de aprovação, precisão e recall; custo de revisão desnecessária separado. Em todas, informar casos aplicáveis, erros de formato, abstenções e cobertura. Denominador zero = N/A, não 100%.

## Saída da análise

Relatório por módulo e fluxo com: fonte do baseline; método e amostra; resultados dos cinco indicadores; diagnósticos; limitações; recomendação de continuar, ajustar ou adiar. Sem implementação, tempo e custo assistidos continuam “não medidos”. Sem ensaio de uso, adoção continua “não medida”. Resultados de simulação não autorizam implantação real.

## Ajuste para fluxo integrado — 23/11/2026

Usar [contrato consolidado](contratos/05-painel-fluxo-integrado.md) e separar as análises:

- **Individual:** cada módulo é chamado diretamente nos casos aplicáveis do dataset individual; expectativas existentes permanecem.
- **Integrada:** unidade principal é uma passagem do caso por uma versão de entrada. Registrar rota, módulos previstos, executados, pulados e falhos. Reentrada é nova passagem; reportar também custo/tempo acumulado do caso para não ocultar retrabalho.
- **Denominadores:** qualidade de módulo inclui suas chamadas previstas; saída corretamente pulada não entra como erro nem acerto individual. Módulo obrigatório indevidamente pulado é falha da integração e permanece no denominador de passagens. Falhas técnicas e abstenções não são removidas.
- **Resultado do fluxo:** passagem correta tem rota correta, slots coerentes, saídas exigidas válidas e próximas ações adequadas. Não exigir parecer quando o desenho prevê complementação ou especialista.
- **Tempo/custo:** somar consumo real da passagem e tentativas, sem duplicar o tempo compartilhado entre módulos. Separar tempo humano ativo no painel, latência do agente e espera externa pelo segurado/especialista. Não converter espera não observada em economia.
- **Adoção:** medir aproveitamento da sugestão da rota/parecer realmente prevista, registrando concordância, discordância, motivo e correção. Ausência indevida de saída permanece no denominador. Decisão humana não é automaticamente verdade de referência: divergências exigem revisão.
- **Segurança:** pagamento após sugestão sem decisão humana é falha crítica de integração; verificar somente com sistema simulado. Também são críticas perda da versão de evidência, uso de aprovação antiga em nova passagem e exposição de conclusão obsoleta como atual.

Ficha adicional: [medicoes-fluxo-template.csv](../data/medicoes-fluxo-template.csv), sem linhas de resultados. Estados e ações humanas têm códigos distintos para complemento ao segurado e análise manual interna. A avaliação operacional real continua fora do que estes testes comprovam.
