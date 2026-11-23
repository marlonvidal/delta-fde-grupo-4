# Avaliações do fluxo integrado

Versão 0.1.0 · 23/11/2026 · **10 cenários sintéticos aprovados por Alex em 23/11/2026**, não resultados medidos. Complementam os 30 testes individuais aprovados sem alterar seus rótulos.

## Casos

| ID | Verificação |
|---|---|
| INT-001 | Ramo comum executa os quatro módulos |
| INT-002 | Foto ausente termina após triagem, aguardando solicitação humana |
| INT-003 | Suspeita leva a especialista; parecer/recomendação não executados |
| INT-004 | Conflito de valores encaminha para análise manual por incerteza |
| INT-005 | Fora do escopo não é negativa |
| INT-006 | Nova versão com foto segue ao ramo comum, preservando histórico |
| INT-007 | Nova versão sem evidência suficiente continua em complementação |
| INT-008 | Discordância humana muda próximo passo, sem reescrever sugestão |
| INT-009 | Aprovação e valor humanos registrados; apenas precondição sintética de pagamento, sem transação |
| INT-010 | Timeout na triagem interrompe fluxo sem aprovação |

`casos.jsonl` contém entrada, snapshot esperado e metadados do avaliador. Entregar **somente `entrada`** ao agente/orquestrador sob avaliação. Snapshot, título, caso de origem e resultado da precondição ficam separados no avaliador. Campos `decisao_humana` e falhas técnicas das fixtures são eventos de teste injetados pelo executor do ensaio, não instruções ao modelo.

Os exemplos em `exemplos/` são snapshots completos escritos para referência, não respostas obtidas de um agente. Saídas de módulo ainda devem passar pelos contratos 0.2.0. A montagem do snapshot não substitui a implementação de um orquestrador.

## Validação

```sh
python3 scripts/validar_fluxos.py
```

Verifica estrutura, referências, consistência de rota, não execução dos ramos, versões/hashes de reentrada, vínculo da decisão humana, preservação de sugestão e controles negativos. O predicado de pagamento não valida identidade, não acessa sistemas e não envia dinheiro. Registros humanos presentes nas fixtures são inteiramente sintéticos.

As rotas de incerteza e fora do escopo para análise manual são propostas explícitas; o pós-revisão especializada continua pendente. O fluxo não inventa retomada desse ramo.

## Avaliação real futura

- Comparar a rota e os slots esperados por etapa, não obrigar quatro execuções em todas as passagens.
- Um módulo corretamente não executado fica fora da métrica de qualidade individual; a não execução correta é avaliada no roteamento integrado.
- Se uma etapa obrigatória for pulada indevidamente, contar como falha de integração, nunca removê-la para melhorar o resultado.
- Abstenção é saída de módulo executado; falha técnica é distinta. Custos e tempos de tentativas falhas continuam no fluxo.
- Reentrada deve usar as evidências da nova versão; dados posteriores não entram no teste de uma passagem anterior.
- A coleta humana e de agente real continua pendente.

## Aprovação dos cenários

Alex revisou e aprovou individualmente INT-001 a INT-010 em 23/11/2026. Status das fixtures: `APROVADO_POR_ALEX`. Aprovação dos comportamentos esperados não representa execução bem-sucedida de agente, validação de regras reais ou aceite técnico de terceiros. O pós-revisão especializada permanece sem retomada automática definida, conforme INT-003 aprovado.
