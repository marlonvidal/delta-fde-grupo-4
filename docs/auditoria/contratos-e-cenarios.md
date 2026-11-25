# Auditoria dos contratos e cenários documentais

24/11/2026 · Auditoria local da especificação; sem chamada de agente, alteração de Langfuse ou publicação no GitHub.

## Conclusão

Os 15 cenários cabem nas categorias de documentação, triagem, parecer e recomendação existentes. O pacote ainda não era uma interface completa para o chat: o contrato principal descreve dados normalizados, enquanto os lotes novos contêm textos ou arquivos nativos. Nenhum adaptador ou extrator conecta esses envelopes automaticamente.

As divergências e lacunas abaixo foram tratadas com correções documentais, uma proposta aditiva de ingestão, matriz de rastreabilidade e controles de contrato. Os schemas individuais 0.2.0 e painel 0.1.0 foram preservados; não é uma migração silenciosa dos consumidores existentes.

## Achados e tratamento

| ID | Achado | Tratamento local | Situação |
|---|---|---|---|
| AUD-01 | Contrato de documentação usa `requisito_id`, schema usa `criterio_id`; descrição omitira `descricao` | Corrigir o contrato para o schema publicado | Corrigido |
| AUD-02 | Entrada comum `dados/evidencias` difere de `contexto/documentos/imagens` e de arquivos nativos | Documentar ponte e publicar schemas de transporte e resultado de ingestão, versão proposta 0.1.0 | Especificado; adaptador pendente |
| AUD-03 | Os dez casos MMV não tinham `status_execucao` explícito nos critérios; os critérios continuam parciais, não saídas completas | Incorporar status aceitos por Alex ao gabarito 0.2.2; preservar revisão visual de Alex registrada | Aceito por Alex; atualização live registrada após conferência |
| AUD-04 | Cinco casos do piloto têm quatro expectativas individuais, mas só FDE-001 executa quatro módulos no fluxo | Tornar seleção dos módulos explícita na matriz; campos dos módulos pulados não são respostas esperadas do fluxo | Esclarecido |
| AUD-05 | O validador de saídas assume inventário `evidencias`; não valida os novos envelopes diretamente | Documentar que IDs novos e R-COB precisam de normalização/proveniência | Implementação pendente |
| AUD-06 | R-COB aparece nas condições quando fornecidas; não pertence ao catálogo operacional inline | Registrar fonte por caso e impedir cópia da regra em FDE-004 | Rastreado; normalização pendente |
| AUD-07 | Vigência inválida foi mantida em análise comum em MMV-010; R-DOC exige vigência e a regra de triagem distingue falta documental de cobertura contradita | Aplicar decisão 2A; alinhar FDE-017/FDE-018 ao MMV-010 | Decisão 2A confirmada |
| AUD-08 | Sem envelope que distinga ausência, ilegibilidade, formato não suportado e falha de extração | Schema/contrato de ingestão e controles negativos, sem misturar status com os módulos | Proposta aditiva |
| AUD-09 | Retorno de complemento era descrito, mas faltava política para retorno do especialista e resolução humana da incerteza | Registrar transições permitidas/pendentes sem inventar retomada automática | Retorno ao analista confirmado (1A); resolução de incerteza/backend pendentes |
| AUD-10 | Os 15 casos não cobrem falhas de ingestão; as 12 variantes exercitam só dois casos de negócio | Separar testes de formato, domínio e transições; não somar como cobertura independente | Documentado |
| AUD-11 | README principal ainda descrevia `src/evals/casos.jsonl` como vazio | Atualizar comandos e apontar os lotes reais | Corrigido |

## O que Samuel recebe como base

- [Catálogo dos 15 casos](catalogo-15-casos.md), com rota, módulos e status esperados.
- [Matriz estruturada](../../src/evals/ingestao/rastreabilidade-15-casos.json), com IDs, fontes e regras.
- [Contrato de ingestão](../contratos/06-chat-ingestao-documental.md), schemas e exemplos parciais de evento/resultado.
- [Contrato do fluxo](../contratos/05-painel-fluxo-integrado.md), com transições e pendências de retomada.
- Contratos individuais e schemas de saída existentes continuam sendo a interface de domínio após normalização.

## Critérios para fechar esta revisão

1. Samuel confirmar adaptação das entradas, registro da regra de cobertura e localização das evidências.
2. Decisões concluídas: status MMV aceitos por Alex; vigência 2A confirmada por Samuel/Breno. Preservar versão e registro dos aceites.
3. Implementar retorno do especialista ao analista sem retomada automática; definir resolução de incerteza, identidade dos atores, concorrência e idempotência.
4. Revisão visual/documental concluída por Alex em 24/11/2026 e sincronizada no Langfuse; validação do agente e revisão independente continuam separadas.
5. Após aprovação das mudanças, atualizar fixtures e referências de Langfuse de forma versionada e consistente.

A consolidação de 24/11/2026 aplica os status MMV aceitos por Alex e sincroniza a revisão 0.2.2 no Langfuse após leitura de conferência. Os datasets continuam separados; não houve execução de agente.

## Fronteira do produto confirmada

Samuel esclareceu que a solução analisa sinistros já abertos no sistema existente. O chat é uma interface de demonstração. O contrato de ingestão pode receber anexos da integração existente; não se implementa abertura de sinistro. Aceite 4B de Alex mantém os formatos no escopo de leitura, não torna o chat um processo operacional obrigatório.

## Aceite visual e documental — 24/11/2026

Alex confirmou a inadequação de MMV-012 por desfoque e MMV-013 por subexposição, e confirmou dano no vidro visível e documentos coerentes nos casos de foto adequada. Revisão registrada por Alex, sem revisão independente ou execução do agente. Esta atualização encerra a pendência local de revisão visual; aceite sincronizado no Langfuse e conferido pela API em 24/11/2026.
