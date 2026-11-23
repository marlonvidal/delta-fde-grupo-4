# Contrato do painel e fluxo integrado

Versão 0.1.0 · 23/11/2026 · complemento aos contratos individuais 0.2.0.

## Evidência e escopo

**Decisão informada por Alex:** o grupo aceitou os diagramas e a proposta de Samuel para um painel de apoio ao analista com automação nível 2. Conferência e triagem precedem os ramos de complementação, análise comum e revisão especializada. Parecer e recomendação seguem no ramo comum; a pessoa decide e define eventual valor. Pagamento ocorre em sistema externo após aprovação humana.

**Recomendação de implementação deste contrato:** usar um snapshot consolidado produzido pelo orquestrador, com as respostas originais dos módulos e a situação do fluxo. Esse envelope não é uma quinta conclusão autônoma de IA. Estados de painel são derivados por regras e, posteriormente, por registros humanos autenticados.

As rotas de incerteza e fora do escopo, já existentes nos contratos individuais, são encaminhadas para análise manual nesta proposta. O comportamento após revisão especializada continua pendente; não se presume aprovação, pagamento nem retorno automático.

## Resposta consolidada

Schema: [painel.schema.json](../../src/evals/schemas/painel.schema.json). Exemplos: [pasta de snapshots](../../src/evals/integrados/exemplos/). Objeto fechado, todos os campos declarados obrigatórios.

| Campo | Significado |
|---|---|
| `versao_fluxo` | Versão deste contrato: 0.1.0 |
| `execucao_id`, `caso_id`, `versao_entrada` | Identificadores da passagem e do caso; versão aumenta quando novas evidências são analisadas |
| `entrada_sha256` | Hash de JSON da entrada, UTF-8, chaves ordenadas, separadores compactos e sem escape ASCII; liga resposta ao conjunto exato de evidências e regras |
| `execucao_anterior_id` | Passagem anterior do mesmo caso, ou null na primeira |
| `gerado_em` | Data/hora com fuso da geração da análise automática; registro humano tem sua própria data posterior |
| `rota`, `situacao_painel` | Encaminhamento automático e situação atual para o analista |
| `resumo`, `evidencias_ids`, `regras_ids` | Explicação e referências válidas desta passagem |
| `modulos` | Os quatro slots, cada um com estado, motivo de não execução e saída original ou null |
| `proxima_acao` | Sugestão ao humano, com código e referências; não representa ação executada |
| `requer_decisao_humana` | Sempre true |
| `decisao_humana` | Registro do backend a partir de ação humana, ou null antes disso; nunca preenchido pelo modelo |
| `pagamento_executado_pelo_agente` | Sempre false |

O painel mostra a saída de cada módulo executado: pendências e verificações em documentação; gatilhos em triagem; afirmações, limites e conclusão no parecer; critérios e motivos em recomendação. Slots não executados são exibidos como tal, sem parecer fictício. Para rotas interrompidas, o painel ainda apresenta evidências e justificativa da conferência/triagem disponíveis.

## Estados dos módulos

- `EXECUTADO`: saída válida presente; pode ter `INSUFICIENTE` ou `FORA_ESCOPO`. Não significa sucesso do sinistro.
- `NAO_EXECUTADO`: `saida=null`, motivo `DESVIO_DE_ROTA` ou `FALHA_ANTERIOR`. Não criar resposta de módulo que não foi chamado.
- `FALHA`: saída de erro produzida pelo executor, com status `ERRO_EXECUCAO` ou `ENTRADA_INVALIDA`; demais módulos posteriores não são chamados.

Os status de execução dos contratos individuais permanecem iguais. Não adicionar `NAO_EXECUTADO` ao status de saída de um agente: ele pertence ao slot do orquestrador.

## Matriz de roteamento, antes da decisão humana

| Rota | Módulos chamados | Situação no painel | Próxima ação humana |
|---|---|---|---|
| `ANALISE_COMUM` | Documentação, triagem, parecer e recomendação | Aguardando analista | Revisar e decidir |
| `COMPLEMENTACAO_DOCUMENTAL` | Documentação e triagem | Aguardando solicitação de complemento | Analista solicita ao segurado |
| `REVISAO_ESPECIALIZADA` | Documentação e triagem | Aguardando encaminhamento ao especialista | Analista encaminha |
| `REVISAO_POR_INCERTEZA` | Documentação e triagem | Aguardando análise manual | Analista resolve incerteza |
| `FORA_ESCOPO` | Documentação e triagem, limitadas ao escopo | Aguardando análise manual | Encaminhar ao responsável apropriado |
| `FALHA_TECNICA` | Até a etapa que falhou, inclusive | Falha técnica | Corrigir e reprocessar sob controle humano |

Parecer ou recomendação com erro interrompem a passagem, sem transformar resultados anteriores em aprovação. Incerteza de documentação pode seguir à triagem para encaminhamento; erro técnico não pode. Não exigir todos os quatro módulos em rotas que saem após triagem.

## Complementação e reentrada

1. O agente recomenda solicitar complemento. A pessoa decide e envia ao segurado por fluxo próprio.
2. A chegada de evidência cria nova versão da entrada e nova execução ligada à anterior. Fotos e regras usadas têm proveniência e disponibilidade temporal.
3. Reexecutar conferência e triagem na nova versão. Só seguir ao parecer/recomendação se a nova rota for comum.
4. Preservar snapshots e decisões anteriores. Uma aprovação antiga não autoriza a nova versão; não copiar automaticamente decisão ou valor.
5. Reentrada deve registrar o evento que a motivou. Atualizar somente o hash sem obter nova evidência não demonstra resolução da pendência.

Os exemplos de reentrada são alternativas de teste: INT-006 e INT-007 partem de INT-002, não constituem duas atualizações consecutivas da mesma execução em produção. A política de concorrência, revisão de versão e deduplicação no backend deve impedir que apenas respostas antigas ou eventos duplicados substituam a versão atual. Esse backend não é implementado neste pacote.

## Ações humanas e significado de “devolver”

Usar códigos diferentes:

- `SOLICITAR_COMPLEMENTO`: pessoa pede documentos/informações ao segurado.
- `ENCAMINHAR_ANALISE_MANUAL`: pessoa analisa internamente; não contata o segurado automaticamente.
- `ENCAMINHAR_ESPECIALISTA`: revisão especializada, sem concluir fraude.
- `APROVAR`: decisão humana registrada; cálculo de indenização é humano.

O registro humano contém decisão, analista pseudônimo no ensaio, data, execução/hash a que se refere, concordância com a sugestão e motivo. Em aprovação pode registrar `valor_aprovado_humano`, string decimal BRL. Esse campo pertence à ação humana, não à resposta do modelo; não reintroduz `valor_recomendado`.

Discordância não altera a recomendação original. A situação do painel e a próxima ação passam a refletir a decisão humana, mantendo a rota automática original para auditoria. Fluxo real exige autenticação e rastreabilidade da ação humana; um campo JSON chamado `REGISTRO_HUMANO` sozinho não comprova identidade ou autorização.

## Pagamento e limites do teste

A sugestão do agente não dispara pagamento. Os testes verificam que uma precondição sintética de pagamento só é satisfeita com aprovação humana associada à execução/hash atual e valor humano válido. Isso é uma verificação local, não implementação de pagamento nem autorização operacional. Alçadas reais, cobertura, autenticação, autorização, idempotência e mecanismo de pagamento ainda pertencem ao sistema responsável.

Nenhuma transação ou mensagem é executada por estes testes. Nenhum resultado de agente é demonstrado pelos snapshots de referência.

## Pendências para integração

- [ ] Samuel confirmar o mapeamento de estados no backend e painel.
- [ ] Definir resultado e retomada após revisão especializada.
- [ ] Confirmar com o grupo as rotas de incerteza e fora de escopo propostas aqui.
- [ ] Definir comportamento para casos de vigência inválida: rótulos individuais 17/18 continuam preservados por aprovação anterior; não foram silenciosamente reclassificados.
- [ ] Implementar eventos, concorrência e deduplicação das decisões humanas no sistema real.
