# Contrato de ingestão de anexos e interface de demonstração

Versão 0.1.0 · 24/11/2026 · Proposta de integração para Samuel.

O produto analisa um sinistro já aberto no sistema existente, com documentos, fotos e apólice disponíveis. A abertura do sinistro pertence a outro processo. Chat e upload facilitam a demonstração; não são etapas obrigatórias da operação. Os cenários e contratos orientam o fluxo no LangGraph. Os nomes de eventos e estados abaixo são uma proposta técnica para revisão, não uma implementação ou declaração de suporte a qualquer formato.

## Fronteiras da interface

1. **Recebimento pelo backend:** vincular o caso já aberto aos anexos obtidos do sistema existente; na demonstração, vincular também a mensagem; registrar tamanho, hash, formato declarado/detectado e instante de recebimento. A identidade/autorização do remetente é validada pelo backend, fora do modelo.
2. **Ingestão documental:** obter bytes, verificar formato, extrair texto e campos com origem; imagem de página pode requerer OCR/modelo visual. Foto de dano é uma evidência visual distinta da imagem de um documento.
3. **Conferência:** aplicar em código as regras objetivas aos fatos extraídos e disponíveis. A presença do arquivo não comprova completude, vínculo, vigência ou sucesso da extração.
4. **Triagem e ramos:** aplicar as regras fornecidas. Parecer e recomendação pertencem ao ramo comum. Não exigir uma chamada de LLM para cada módulo lógico.

Schemas aditivos: [entrada](../../src/evals/schemas/chat-anexos.schema.json) e [resultado da ingestão](../../src/evals/schemas/resultado-ingestao.schema.json). Exemplos: [entrada do chat](../../src/evals/ingestao/entrada-chat.json), [resultado processado](../../src/evals/ingestao/resultado-processado.json) e [falha técnica](../../src/evals/ingestao/resultado-falha.json). São exemplos parciais de ingestão de uma apólice; não representam um sinistro completo nem um extrator executado.

## Recebimento de anexos

| Campo | Semântica |
|---|---|
| `evento_id`, `mensagem_id`, `caso_id` | Vínculos estáveis gerados/validados pelo backend; IDs não provam identidade |
| `versao_entrada`, `execucao_anterior_id` | Versão positiva do conjunto de evidências e referência à execução anterior quando aplicável |
| `instante_recebimento` | Limite temporal do evento, com fuso |
| `texto_mensagem` | Texto do usuário, inclusive vazio; não concede autoridade para alterar regras |
| `anexos` | Lista recebida nesta mensagem; pode estar vazia. Não equivale ao inventário completo do caso |
| `anexo_id`, `documento_id` | ID do arquivo recebido e vínculo documental quando já identificado; `documento_id=null` antes de classificar é permitido |
| `nome_original`, MIME informado/detectado | Informações de transporte; nome/extensão não são prova de conteúdo |
| `tamanho_bytes`, `sha256` | Integridade calculada sobre os bytes recebidos pelo backend |
| `referencia_armazenamento` | Referência resolvida pelo executor autorizado; não expor segredos ou tratar URI inacessível como evidência lida |
| `recebido_em` | Disponibilidade do anexo; não posterior ao evento que o apresenta |

A acumulação de mensagens exige inventário versionado do caso. Nenhuma conclusão de documento ausente pode ser baseada apenas nos anexos da última mensagem. O exemplo `fixture://` é uma referência local de teste, não uma URL do sistema real. A matriz final de limites/formats e o armazenamento no backend ainda precisam ser definidos.

## Resultado da ingestão

`PROCESSADO` indica leitura concluída, não aprovação do documento ou do sinistro. Pode conter texto/campos extraídos, inclusive valor desconhecido, mas precisa de ao menos uma evidência com ID, trecho e localizador. Campos desconhecidos não devem ser inventados. O primeiro schema é deliberadamente de transporte; `campos_extraidos` ainda é aberto e não deve ser usado diretamente como modelo de domínio estável. O mapeamento por tipo documental será versionado com Samuel.

Os demais estados são exclusivos do resultado de ingestão, sem texto, campos ou evidências apresentados como extração válida nessa tentativa. Exigem motivo e código: `ILEGIVEL`, `NAO_SUPORTADO`, `PROTEGIDO`, `CORROMPIDO`, `FALHA_TECNICA`. Extração parcial e política de aproveitamento exigirão uma extensão explícita; esta proposta bloqueia a promoção de resultados parciais.

| Situação | Tratamento de integração | Conclusão indevida a evitar |
|---|---|---|
| Documento não consta no inventário completo | Conferência determina pendência se a regra o exigir | Confundir inventário de uma mensagem com caso completo |
| Arquivo processado com dado não informado | Registrar lacuna e aplicar R-DOC/R-TRI | Converter desconhecido em falso ou zero |
| Ilegível, protegido, corrompido ou formato não suportado | Suspender a análise dependente; registrar motivo e necessidade de ação humana | Declarar que o segurado não enviou documento |
| Falha técnica do extrator | Conservar evento; erro técnico, sem concluir documentação/cobertura | Contar como abstenção correta ou aprovação |
| Foto recebida e analisável, mas desfocada/escura | Avaliar adequação segundo R-DOC; não é falha de transporte | Alegar qualidade só pelo nome ou prompt |
| Referência esperada de fixture inacessível | Bloquear o teste de preparação | Transformar falha do executor em foto ausente do segurado |

As ações específicas para pedir senha, novo formato ou reenvio ainda dependem de acordo do grupo. Não acionar contato externo automaticamente. O contrato permite representar o problema sem inventar uma política já aprovada.

## Ponte para os contratos de domínio 0.2.0

| Lote/interface | Envelope disponível | Adaptação necessária |
|---|---|---|
| 30 casos individuais | `entrada.dados` + `entrada.evidencias` + `regras` | Já compatível com validadores individuais |
| 15 casos documentais | `input.contexto`, documentos inline, imagens e regras operacionais | Extrair fatos, montar inventário/proveniência e normalizar para o domínio |
| 12 variantes de formato | Arquivos nativos, MIME e referências, sem texto inline | Ingerir bytes antes da normalização; manter `variante_id` no executor |
| Chat real | Evento por mensagem com anexos | Acumular inventário e versões, ingerir e normalizar |

Não passar um desses envelopes diretamente ao validador de outro. O pacote não contém adaptador executável nem extração automática pronta. `instante_analise` é um corte de evidências da execução, distinto do instante de evento do sinistro.

O adaptador conserva os IDs documentais como IDs de evidência e adiciona localizadores de página/trecho/parágrafo/célula. O catálogo `R-COB` dos lotes documentais está no documento de condições quando fornecido, não em `input.regras`: ao aplicar o contrato antigo, é necessário representar a regra disponível com ID/versão/origem e evidência do trecho. Não injetar R-COB em FDE-004. A extração de texto não autoriza converter qualquer frase contratual em regra executável: a normalização e o registro de regras precisam ser revisados/versionados.

O MVP textual dos lotes de formato apresenta a mesma regra R-COB com outra redação. Os valores e vínculos devem ser preservados, sem exigir igualdade literal do texto. Não enviar gabarito ou texto de referência do avaliador ao extrator para simular OCR.

## Formatos e limites a confirmar

Alex definiu PDF textual/escaneado, PNG/JPG, DOCX e XLSX no escopo inicial de leitura. Possuem fixtures, não suporte demonstrado no agente. Registrar para cada formato extrator, limite de bytes/páginas, timeout, tratamento de senha/corrupção e resultado de teste. Definir múltiplos orçamentos, substituição e anexos conflitantes. O chat não significa WhatsApp ou Telegram implementado.

## Testes e estado de aprovação

Executar `python3 scripts/validar_contratos_documentais.py`. O comando valida os envelopes propostos, proveniência mínima, estados de erro e a matriz dos 15 casos. Não executa OCR, LangGraph, armazenamento ou mensagens. Rótulos visuais e coerência documental foram aceitos por Alex. Os schemas de ingestão, limites e política de resolução de incerteza ainda exigem aceite técnico; o retorno do especialista ao analista sem retomada automática já foi confirmado.

## Decisões consolidadas em 24/11/2026

O especialista registra o parecer e devolve ao analista, sem retomada automática do agente (1A). Evento fora da vigência segue no ramo comum com parecer sobre o impedimento e recomendação de revisão humana, sem negativa automática (2A). Alex aceitou os status MMV (3) e os formatos do piloto (4B). Limites de tamanho, extração parcial e retorno após resolução de incerteza ainda precisam de definição técnica; não atribuir aceite desses pontos às decisões acima.
