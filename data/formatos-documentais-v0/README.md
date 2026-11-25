# Variantes de formatos documentais

Lote local 0.2.0: **2 casos de negócio, 12 variantes e 42 arquivos**. FDE-001 testa documentação consistente e análise comum; FDE-003 preserva a divergência aviso R$ 2.300,00 versus orçamento R$ 1.800,00 e revisão por incerteza. Os 15 casos anteriores não foram modificados. Importação no Langfuse autorizada por Alex e verificada pela API. Nenhuma execução do agente ou push nesta etapa.

## Matriz de formatos

| Variante | Documentos recebidos | Processamento a verificar |
|---|---|---|
| PDF-TEXTO | Quatro PDFs com texto selecionável | Extração de texto e normalização |
| PDF-ESCANEADO | Quatro PDFs de uma página raster, sem camada de texto | OCR ou modelo visual |
| PNG | Quatro imagens de páginas documentais | OCR ou modelo visual |
| JPG | Quatro imagens JPEG de páginas documentais | OCR ou modelo visual |
| DOCX | Quatro documentos Word | Extração de parágrafos |
| XLSX | Orçamento em planilha e demais documentos em PDF textual | Leitura de células e moeda |

Cada variante preserva os fatos de negócio do caso original; redação e diagramação foram adaptadas ao tipo documental. As imagens PNG/JPG aqui são páginas de documentos, não fotos de danos. A fotografia do dano permanece vinculada ao caso original no piloto e não é duplicada neste lote. XLSX é um conjunto misto deliberado: só o orçamento vira planilha.

## Contrato de entrada

`entradas.jsonl` contém `input` e `metadata`. O campo `documentos` do input referencia arquivos reais, seus IDs, tipos e MIME, sem texto extraído inline. Os caminhos documentais são relativos a este lote. Os caminhos de `imagens` (fotos de danos) são relativos à raiz do repositório. O adaptador deve resolver essas bases explicitamente, obter os bytes e não fornecer o gabarito ao agente. IDs de variante e formato ficam nos metadados. O `caso_id` de negócio permanece o mesmo: o executor identifica uma execução por `variante_id`, não somente pelo caso.

`avaliador/verdade.jsonl` separa extração documental, texto de referência e comportamento esperado. O texto de referência é exclusivo do avaliador: a execução de OCR não pode recebê-lo. Cada família fica integralmente em DESENVOLVIMENTO; variantes quase idênticas não podem ser separadas em treino e avaliação reservada.

## Critérios de aceitação

- Extrair identificadores, datas, vínculos, moeda, valores e informações materiais sem omitir negações.
- Manter R$ 1.800,00 no orçamento de ambos os casos; no FDE-003, manter os R$ 2.300,00 do aviso.
- Preservar rota e critérios de negócio do caso original quando a extração for suficiente.
- Não usar nome do arquivo como evidência de conteúdo. A presença de um arquivo não comprova sucesso da extração.
- Falha de leitura, formato não suportado e informação desconhecida são condições distintas. Não aprovar com dados presumidos nem confundir erro de processamento com documento não enviado.

Os arquivos são sintéticos e rasterizados de forma limpa a 150 dpi. Não representam fotografias reais de papel nem comprovam desempenho de OCR. Os gabaritos e o suporte de cada formato dependem de revisão com Samuel. Arquivos corrompidos, protegidos por senha, limites de tamanho e formatos não suportados ficam para a próxima bateria, após definir os estados e respostas esperados.

## Verificação local

`python3 scripts/validar_formatos_documentais.py`

O validador confere inventário, hashes, vínculos, presença/ausência de camada textual em PDFs, conteúdo do DOCX, valores de orçamento no XLSX e separação de entrada/gabarito. Isso não executa OCR nem mede o agente.

## Apresentação dos documentos

Apólice com identificação e vigência; aviso com registro da ocorrência; orçamento com serviço, vínculos e total; condições com disposições de cobertura. Cabeçalhos e tabelas substituem o TXT corrido. A identificação de teste fica em rodapé discreto. Não foram adicionadas franquias, exclusões, assinaturas ou regras de cobertura além do cenário. Os gabaritos de extração refletem a redação apresentada; IDs, datas e valores foram conferidos contra os originais.

## Importação no Langfuse

Dataset: [amparo-formatos-documentais-v0](https://us.cloud.langfuse.com/project/cmwtuztw500wjad0d8k6znpmu/datasets/cmwur285z0024ad0enk1ra31p). Doze variantes, 42 arquivos documentais e duas fotos de dano reutilizadas. Arquivos nativos acessíveis por referências de mídia; texto do avaliador permanece separado da entrada. Bytes recuperados e hashes SHA-256 conferidos após upload. O recebimento dos arquivos não valida OCR, suporte do agente ou gabaritos.
