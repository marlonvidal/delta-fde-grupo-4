# Contrato 4 — Recomendação para decisão humana

Versão 0.2.0 · **Proposta**. Aplicam-se as [regras comuns](README.md).

## Objetivo e entrada

Recomendar aprovação ou revisão humana com fundamento verificável, sem aprovar, negar ou pagar. Receber dados e evidências do caso, regras de elegibilidade/cobertura e limites de recomendação. Parecer e triagem podem ser fornecidos, mas não substituem evidências originais.

## Regra de decisão proposta

1. Fora do escopo explícito: `REVISAO_HUMANA`, motivo `FORA_ESCOPO`, status `FORA_ESCOPO`.
2. Informação ou regra essencial ausente, conflito não resolvido ou acesso insuficiente: `REVISAO_HUMANA`, motivo correspondente, status `INSUFICIENTE`.
3. Critério explícito de aprovação não atendido ou exceção definida: `REVISAO_HUMANA`, status `CONCLUIDO` se houve evidência suficiente para essa avaliação. Não recomendar negativa automática.
4. Somente quando todas as condições explícitas e necessárias forem atendidas, regras estiverem declaradas completas e não houver exceção: `RECOMENDAR_APROVACAO`, status `CONCLUIDO`.

A alçada de até R$ 5.000 é limite do processo atual, não condição suficiente de aprovação. O recorte de até R$ 2.000, score baixo e ausência de sinistro anterior é um segmento descrito no case, não uma regra de aprovação validada.

## Saída específica

- `recomendacao`: `RECOMENDAR_APROVACAO`, `REVISAO_HUMANA` ou `null` quando entrada inválida/erro impedir análise.
- `motivos`: lista de códigos definidos no dataset, por exemplo `REGRA_AUSENTE`, `EVIDENCIA_INSUFICIENTE`, `CONFLITO`, `CRITERIO_NAO_ATENDIDO`, `EXCECAO` e `FORA_ESCOPO`.
- `criterios_verificados`: lista de regra, resultado (`ATENDIDO`, `NAO_ATENDIDO`, `DESCONHECIDO`) e evidências.
- `decisao_executada`: sempre `false`.
- `proximas_acoes`: passos propostos ao analista, com evidências/regras disponíveis; obrigatórios quando houver impedimento.

Não existe campo `valor_recomendado` nesta versão. O módulo recomenda apenas elegibilidade; regra de cálculo ausente não impede uma recomendação de aprovação quando os demais critérios explícitos estiverem atendidos. Cálculo da indenização e decisão final são humanos.

## Cenários de aceitação propostos

| Entrada | Esperado |
|---|---|
| Regras completas de teste e todos os critérios atendidos | Recomendar aprovação, com referências; decisão não executada |
| Apenas valor baixo e score baixo | Revisão por evidência/regra insuficiente |
| Evidência obrigatória ausente | Revisão; nunca recomendação de aprovação |
| Critério de cobertura explicitamente não atendido | Revisão com motivo; não efetivar negativa |
| Parecer anterior recomenda aprovação sem suporte | Verificar origem e encaminhar à revisão |
| Valor acima de R$ 5.000 | Fora do escopo, revisão humana |
| Orçamento presente, cálculo de indenização ausente | Recomendar elegibilidade se demais critérios atendidos; cálculo fica humano |

## Avaliação e limites

Unidade: caso. Matriz de confusão binária em casos julgáveis; positivo = `RECOMENDAR_APROVACAO`, negativo = `REVISAO_HUMANA`. Falso positivo é aprovação recomendada quando a revisão era necessária. Falso negativo é revisão quando as regras permitiam recomendar aprovação; pode elevar trabalho humano e deve ser medido.

Avaliar motivos e critérios separadamente. Reportar aprovação indevida, precisão das recomendações de aprovação, recall, taxa de revisão/abstenção e tempo humano. Entrada inválida e erro técnico são falhas separadas, não acertos negativos. Caso sem resposta esperada validada fica `NAO_AVALIAVEL` no avaliador, sem ser usado para calcular acurácia.

**Falhas críticas propostas:** recomendar aprovação sem requisito essencial ou contra regra explícita; sugerir valor de indenização; executar ou alegar aprovação, negativa ou pagamento; contornar a etapa humana.

**Pendências:** regras completas de cobertura/elegibilidade, definição de exceções e validação dos rótulos. Até isso existir, testar abstenções e regras simuladas; não declarar validação de aprovação na operação real.
