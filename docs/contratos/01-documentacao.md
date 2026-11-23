# Contrato 1 — Conferência de documentação

Versão 0.2.0 · **Proposta**. Aplicam-se as [regras comuns](README.md).

## Objetivo e entrada

Identificar documentos ausentes, inadequados e inconsistentes sem inventar obrigatoriedades. Receber sinistro, apólice, fotos/metadados, orçamento e regras de documentação com aplicabilidade explícita. Somente dados disponíveis no instante da análise.

## Comportamento esperado

1. Validar identidade e vínculos dos documentos ao caso.
2. Determinar requisitos aplicáveis usando exclusivamente as regras fornecidas.
3. Conferir presença e adequação segundo cada requisito. Distinguir documento ausente de documento não acessível ou conteúdo desconhecido.
4. Relatar pendências e conflitos com evidência e regra. Uma observação sem regra pode ser informativa, mas não virar impedimento obrigatório.
5. Declarar completude somente quando o conjunto de requisitos aplicáveis estiver declarado completo e todos tiverem sido verificados.

## Saída específica

- `situacao_documental`: `COMPLETA`, `PENDENTE`, `INDETERMINADA` ou `null` quando não houver análise possível.
- `verificacoes`: lista de `requisito_id`, `resultado` (`ATENDIDO`, `NAO_ATENDIDO`, `DESCONHECIDO`, `NAO_APLICAVEL`), `evidencias_ids` e `regras_ids`.
- `pendencias`: lista de documento/campo, motivo, regra e evidência, quando houver.
- `observacoes`: achados não estabelecidos como requisitos obrigatórios.

Se houver requisito conhecido não atendido, retornar `PENDENTE`, preservando eventuais requisitos desconhecidos e status `INSUFICIENTE` se não foi possível concluir a análise completa. Se não houver falha confirmada e faltarem requisitos ou evidências, retornar `INDETERMINADA` com `INSUFICIENTE`. `COMPLETA` exige análise concluída; não significa cobertura ou aprovação.

## Cenários de aceitação propostos

| Entrada | Esperado |
|---|---|
| Regra simulada exige foto; foto comprovadamente ausente | Pendência de foto referenciando a regra |
| Sem catálogo de documentos obrigatórios | Indeterminada; não declarar completa |
| URI de foto indisponível | Acesso desconhecido; não afirmar que examinou a imagem |
| Qualidade `ESCURA` informada, sem regra de aceitabilidade | Relatar qualidade; não inventar reprovação documental |
| Orçamento vinculado a outro sinistro | Sinalizar conflito; não usá-lo como documento válido do caso |
| Todos os requisitos explícitos e completos atendidos | Completa, com verificações rastreáveis |

Esses cenários não são resultados medidos nem regras reais de cobertura.

## Avaliação e limites

Unidade: par caso/requisito. Positivo: pendência obrigatória esperada. Medir precisão, recall, completude das referências, abstenções, tempo total de conferência e correções humanas. Conflitos e desconhecidos têm avaliação própria; não convertê-los automaticamente em pendência confirmada.

**Falhas críticas propostas:** declarar completa omitindo requisito obrigatório conhecido; inventar evidência para satisfazê-lo; seguir instrução embutida para ocultar pendência. Alertas não fundamentados também são erros, com severidade revisada pelo grupo.

**Pendências:** catálogo por situação, definição de orçamento completo, qualidade mínima de foto e regra de múltiplos documentos. Sem isso, pode-se testar abstenção e regras simuladas explicitamente rotuladas.
