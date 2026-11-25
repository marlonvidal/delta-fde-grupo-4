# Contrato 2 — Triagem

Versão 0.2.0 · **Proposta**. Aplicam-se as [regras comuns](README.md).

## Objetivo e entrada

Recomendar o encaminhamento do sinistro sem decidir cobertura ou fraude. Receber dados do caso, evidências, regras de triagem e, opcionalmente, conferência documental com proveniência. O módulo deve funcionar sem depender de outro agente quando receber os dados necessários.

## Categorias e precedência propostas

Aplicar a primeira condição satisfeita; preservar achados secundários:

1. `FORA_ESCOPO`: limite explícito do módulo não atendido, como valor acima de R$ 5.000 no escopo deste exercício. Não negar o sinistro.
2. `REVISAO_ESPECIALIZADA`: gatilho de encaminhamento especializado explicitamente definido e sustentado por evidência.
3. `REVISAO_POR_INCERTEZA`: regra ausente, conflito relevante ou dado desconhecido impede escolher com segurança as demais filas.
4. `COMPLEMENTACAO_DOCUMENTAL`: pendência obrigatória comprovada e nenhuma condição anterior.
5. `ANALISE_COMUM`: regras de triagem completas e nenhuma condição anterior.

Se a entrada não puder ser interpretada, categoria `null` e `ENTRADA_INVALIDA`. Incerteza retorna categoria `REVISAO_POR_INCERTEZA` e status `INSUFICIENTE`; fora do escopo usa status correspondente. Demais categorias usam `CONCLUIDO` quando os critérios foram verificados. Não usar pontuação arbitrária de risco ou desempate inventado.

## Saída específica

- `encaminhamento`: uma categoria acima ou `null`.
- `gatilhos`: lista de condição, regras e evidências.
- `achados_secundarios`: condições adicionais relevantes, inclusive pendências documentais.

## Cenários de aceitação propostos

| Entrada | Esperado |
|---|---|
| Valor R$ 5.000, regras completas e sem outros gatilhos | Não marcar fora do escopo apenas pelo valor |
| Valor R$ 5.000,01 | Fora do escopo deste módulo; sem negativa |
| Gatilho especializado explícito e foto obrigatória ausente | Revisão especializada; foto como achado secundário |
| Regra de prioridade ausente ou conflito impeditivo | Revisão por incerteza |
| Somente documento obrigatório ausente, demais verificações completas | Complementação documental |
| Dados e regras completos, sem exceção | Análise comum |
| Score baixo de modelo fora da população de calibração | Não usar como autorização; sinalizar limitação conforme regras disponíveis |

## Avaliação e limites

Unidade: caso. Matriz de confusão multiclasse, recall de revisão especializada e taxa de envio indevido à análise comum. Reportar cobertura, abstenções e erros de execução separadamente. Se o esperado for incerteza, classificá-la corretamente não é falha de encaminhamento; ainda deve aparecer na taxa de abstenção.

**Falhas críticas propostas:** enviar à análise comum caso com gatilho especializado explícito; tratar score como fraude confirmada; executar encaminhamento externo ou decisão operacional fora deste contrato.

**Pendências:** grupo validar nomes das filas, gatilhos e precedência. Sem regras completas, não rotular casos como análise comum apenas porque nenhum problema foi informado.

## Vigência e fronteira do fluxo — decisão de 24/11/2026

Evento comprovadamente fora da vigência segue `ANALISE_COMUM`, quando não houver condição de maior precedência, para parecer explicitando cobertura contradita e recomendação `REVISAO_HUMANA`. Não tratar esse impedimento como documento ausente que possa ser resolvido por reenvio. FDE-017/FDE-018 e MMV-010 foram alinhados à decisão 2A. O especialista devolve seu parecer ao analista, sem retomada automática (1A).
