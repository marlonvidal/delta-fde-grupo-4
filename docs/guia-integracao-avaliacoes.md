# Guia de integração para Samuel

20/11/2026 · contratos de saída **0.2.0** · dataset **0.3.0**.

## Decisões de Alex

Os quatro módulos fazem parte do escopo inicial: documentação, triagem, parecer e recomendação. As respostas serão usadas em tela e integração. Próxima ação humana é obrigatória quando houver impedimento. Incerteza usa motivos objetivos; não há percentual de confiança. Recomendação tem somente aprovação de elegibilidade ou revisão humana, sem negativa e sem valor de indenização. Nenhuma ação operacional é executada.

Alex aprovou os cenários e autorizou os ajustes coerentes com estas decisões. Isso não atribui aceite técnico a Samuel nem converte regras simuladas em condições reais de seguro.

## Arquivos de implementação

| Módulo | JSON Schema autocontido | Exemplo inicial |
|---|---|---|
| Documentação | [documentacao.schema.json](../src/evals/schemas/saidas/documentacao.schema.json) | [FDE-001](../src/evals/exemplos-saida/FDE-001.documentacao.json) |
| Triagem | [triagem.schema.json](../src/evals/schemas/saidas/triagem.schema.json) | [FDE-001](../src/evals/exemplos-saida/FDE-001.triagem.json) |
| Parecer | [parecer.schema.json](../src/evals/schemas/saidas/parecer.schema.json) | [FDE-001](../src/evals/exemplos-saida/FDE-001.parecer.json) |
| Recomendação | [recomendacao.schema.json](../src/evals/schemas/saidas/recomendacao.schema.json) | [FDE-001](../src/evals/exemplos-saida/FDE-001.recomendacao.json) |

Há 20 exemplos completos: os cinco casos iniciais × quatro módulos, na pasta `src/evals/exemplos-saida/`. São respostas de referência escritas para demonstrar o contrato, não resultados de um agente. O texto pode variar; o sentido e os critérios esperados não.

## Entrada, processamento e saída

1. Ler uma linha de `src/evals/casos.jsonl`.
2. Selecionar um módulo e entregar **somente `entrada`** ao agente. Nunca passar `esperado`, título, tags, justificativa do caso ou exemplos de resposta do caso avaliado.
3. Pedir resposta JSON no schema correspondente, usando contrato 0.2.0. Se o provedor exigir adaptação de formato, manter os mesmos campos e documentar o adaptador. Não há endpoint ou biblioteca de agente impostos por este pacote.
4. Validar estrutura, IDs e invariantes. Não corrigir silenciosamente resposta inválida para transformá-la em acerto. Registrar retentativas e seu custo.
5. Comparar campos objetivos com `esperado`; revisar justificativa, evidências por conclusão e próximas ações pela rubrica humana.
6. Exibir na tela situação, explicação, impedimentos e ações humanas; usar os mesmos campos na integração.

Cada módulo pode funcionar sozinho. Se houver composição, preservar evidências e proveniência: saída anterior não é fato confirmado. Ainda é necessário testar erros em cascata.

## Campos e convenções

Todos os campos declarados são obrigatórios. Objetos são fechados (`additionalProperties: false`), inclusive itens de listas. Usar `[]` para ausência de itens e `null` somente quando explicitamente permitido. Não adicionar `valor_recomendado`, `confianca` ou `percentual_confianca`.

- `justificativa`: explicação legível da conclusão principal, sustentada pelos IDs do envelope.
- `verificacoes` / `criterios_verificados`: itens com `criterio_id`, resultado, descrição e referências.
- `lacunas`, `conflitos`, `pendencias`, `inconsistencias` e `limitacoes`: itens com código, campo afetado, descrição e referências disponíveis.
- `proximas_acoes`: código, descrição, responsável fixo `ANALISTA_HUMANO` e referências disponíveis. Somente sugestões; não chamar sistema externo para executá-las.
- `afirmacoes`: fato, cálculo ou inferência com evidências/regras e fórmula quando houver cálculo. Não calcular indenização, mesmo que outros cálculos factuais possam ser explicados.
- `evidencias_ids` e `regras_ids`: IDs exatos recebidos, por conclusão e no envelope. Dados conhecidos ausentes podem ser demonstrados pelo inventário vazio. Uma regra ausente não tem ID citável: usar lista de regras vazia e explicar em `lacunas`; nunca inventar referência. Falhas técnicas também podem não ter evidência de domínio.

Não é exigida igualdade literal das justificativas. Referências existentes não garantem sustentação semântica: revisar se de fato apoiam a conclusão.

## Status e falhas

| Status | Significado e convenção |
|---|---|
| `CONCLUIDO` | Tarefa concluída; pode ter pendência documental ou recomendar revisão. Não significa sinistro aprovado |
| `INSUFICIENTE` | Dados/regras insuficientes. Documentação pode ser indeterminada, triagem por incerteza, parecer parcial ou recomendação de revisão |
| `FORA_ESCOPO` | Não concluir cobertura. Documentação e cobertura usam `null`; triagem `FORA_ESCOPO`; recomendação `REVISAO_HUMANA` |
| `ENTRADA_INVALIDA` | Executor detecta entrada não interpretável. Resultado específico `null`, listas de domínio vazias e próxima ação para corrigir entrada |
| `ERRO_EXECUCAO` | Executor registra timeout/falha técnica. Resultado específico `null`, sem conclusão de domínio e próxima ação de recuperação pelo operador humano |

Campos de texto do parecer (`resumo`, `conclusao`) aceitam `null` se não houve análise. Falhas técnicas usam `motivos` correspondentes na recomendação e `decisao_executada=false`. Se houver retomada ou retentativa, preservar registro original. Não converter erro em uma revisão humana considerada correta pelo avaliador.

O schema verifica estrutura; `scripts/validar_saidas.py` acrescenta invariantes e checagem de IDs contra a entrada. Essas regras devem acompanhar a integração; copiar somente o JSON Schema não garante coerência entre status e conclusão.

## Como verificar localmente

```sh
python3 scripts/validar_dataset.py
python3 scripts/validar_saidas.py
python3 scripts/validar_saidas.py --resposta src/evals/exemplos-saida/FDE-004.recomendacao.json
```

Os scripts usam biblioteca padrão e um validador explícito do subconjunto de JSON Schema usado aqui, não um motor genérico de todos os recursos do Draft 2020-12. Não desabilitar assertions (`python -O`) ao executar estas verificações. Exemplos são comparados ao gabarito e controles negativos verificam rejeição de negativa, valor sugerido, decisão executada, campos extras, referências inexistentes e impedimento sem ação.

## Telemetria e entrega de implementação

Registrar fora da resposta do modelo: execução, caso, módulo, versão de modelo/prompt/regras/dataset, resposta bruta, status, retentativas, duração, tokens, custo conhecido e revisão humana. Não estimar tokens/custo por autodeclaração do agente. Usar [plano de medição](plano-de-medicao.md).

Para devolver uma versão testável: informar comando ou interface, módulos disponíveis, configuração sem segredos e localização dos logs. Métricas e metas estão no [contrato de sucesso](02-contrato-de-sucesso.md). Ainda não há executor do agente ou resultados medidos neste pacote.

## Mudança desta versão

Removido campo `valor_recomendado` e regra simulada `R-VAL`. FDE-030 agora espera recomendação de elegibilidade quando todos os demais critérios estão satisfeitos; falta de cálculo não é impedimento. Contratos, expectativas, catálogo e entradas do ensaio manual foram atualizados juntos. Os demais rótulos foram preservados, incluindo FDE-017 e FDE-018 conforme aprovação anterior de Alex.


## Complemento de 23/11/2026 — fluxo aceito e painel consolidado

Conforme informado por Alex, o grupo aceitou o fluxo de Samuel. Usar o [contrato do painel](contratos/05-painel-fluxo-integrado.md), o [schema consolidado](../src/evals/schemas/painel.schema.json) e os [10 cenários integrados](../src/evals/integrados/README.md). Contratos individuais 0.2.0 e dataset individual 0.3.0 permanecem válidos.

No teste individual, um módulo recebe a entrada e produz sua saída mesmo quando outro módulo interromperia o fluxo. No teste integrado, a triagem decide o ramo: complementação e revisão especializada não chamam parecer/recomendação nessa passagem. Incerteza e fora do escopo seguem para análise manual na proposta registrada. Não execução por rota é estado do slot do orquestrador, não erro ou abstenção do agente.

O orquestrador monta o painel com as saídas originais e referências. Não fabricar respostas dos módulos pulados. Registro humano pertence ao backend autenticado, não ao modelo. Retorno de documentos cria nova versão e nova passagem ligada à anterior. O pós-revisão especializada ainda precisa ser definido.

Executar também:

```sh
python3 scripts/validar_fluxos.py
```

Os cenários são fixtures, sem orquestrador conectado ou agente executado. Testes de pagamento avaliam apenas precondições sintéticas; não implementam pagamento ou autorização real.
