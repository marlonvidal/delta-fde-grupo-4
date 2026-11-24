# Piloto documental e multimodal — lote local v0.1.0

**Piloto sintético importado no Langfuse, com revisão humana dos rótulos pendente.**

Cinco cenários adaptados do dataset de metadados aprovado (0.3.0). O lote anterior permanece intacto. São **dados inteiramente sintéticos**, não os cinco casos reais mencionados na reunião, que não foram fornecidos nesta etapa.

## Entregas

- `documentos/`: 19 documentos textuais de teste — extrato de apólice, aviso e orçamento em cada caso; condições simuladas em quatro casos. Formato TXT, legível e fácil de consumir pelo agente. Não são PDFs ou teste de OCR.
- `documentos/manifesto.jsonl`: inventário de documentos, vínculo ao caso e hashes SHA-256.
- `imagens/manifesto.jsonl`: quatro imagens planejadas, todas recebidas e com revisão humana pendente. Contém quatro arquivos PNG sintéticos fornecidos por Alex.
- `prompts/`: prompts de referência usados na preparação das imagens.
- `entradas/` e `entradas.jsonl`: dados que o agente poderá receber; texto documental inline e referências locais para fotos.
- `avaliador/verdade.jsonl`: resultados esperados por módulo e fluxo, restritos ao avaliador.
- `revisao.html`: página local com documentos e gabaritos para revisão humana; **não enviar ao agente**.

## Distribuição inicial

| Caso | Diferença intencional | Imagem | Rota esperada após materiais completos |
|---|---|---|---|
| FDE-001 | Dados e regras simuladas atendidos | Recebida; revisar | Análise comum |
| FDE-002 | Foto obrigatória não recebida | Ausência intencional | Complementação |
| FDE-003 | Aviso R$ 2.300; orçamento R$ 1.800 | Recebida; revisar | Revisão por incerteza |
| FDE-004 | Condições de cobertura indisponíveis | Recebida; revisar | Revisão por incerteza |
| FDE-005 | Valor R$ 5.000,01 | Recebida; escopo pode interromper antes da visão | Fora do escopo, revisão humana |

Fotos pendentes de preparação não podem ser tratadas como ausentes no processo do segurado. O executor deve bloquear testes que dependam de imagens ainda não disponibilizadas. FDE-002 testa ausência por definição, não falha de preparação.

## Separação de entrada e gabarito

O agente recebe somente `input` de `entradas.jsonl`. Não recebe rótulos visuais, expectativas, prompts de geração, título do cenário ou notas do avaliador. Referências a arquivos locais precisam ser resolvidas pelo executor para bytes/partes multimodais compatíveis com o modelo; o caminho sozinho não dá acesso à imagem.

O documento de condições é a fonte da cobertura R-COB quando fornecido. No FDE-004 ele foi omitido, sem cópia oculta da cobertura nos outros documentos. As regras operacionais de documentação, triagem e recomendação continuam explicitamente simuladas no input.

O contexto não entrega a qualidade esperada da foto; ela deve ser inspecionada pelo modelo quando houver imagem. O orçamento nomeia o serviço de para-brisa e pode auxiliar a interpretação — isso não substitui verificar a evidência visual. Este lote não isola a classificação de dano por imagem: um experimento visual independente precisará de entradas e casos específicos.

## Critérios esperados são provisórios na nova modalidade

Os resultados herdados do lote de metadados são **critérios de referência**, não respostas completas diretamente compatíveis com o novo envelope. As checagens documentais referenciam os IDs do novo lote; os vínculos devem ser confirmados contra as evidências efetivamente recebidas. O adaptador e as saídas visuais ainda devem ser alinhados com a implementação de Samuel.

Os quatro módulos lógicos podem corresponder a menos nós físicos: conferência em código, triagem e parecer/recomendação com LLM. O lote não exige criar quatro chamadas de modelo nem inferir por LLM regras determinísticas.

Rótulos de imagem ainda são alvos de geração, não fatos confirmados. Alex deve conferir cada imagem produzida, ajustar ou rejeitar o material e revisar as expectativas com um revisor. Não considerar como verdade validada algo apenas porque o gerador recebeu aquele pedido. O lote não representa 12% de fotos ruins ou 7% sem foto na operação; ele foi escolhido para cobertura inicial.

## Uso no Langfuse

A preparação separa o catálogo de imagens, os documentos e a verdade vinculada por caso. Para avaliação end-to-end, a unidade é o caso completo: juntar entrada, mídia acessível e resultado esperado no adaptador de importação. Imagem ou documento isolado só deve virar item de experimento se houver tarefa e avaliação próprias para ele.

Importação autorizada por Alex e conferida por leitura da API: 5 casos, 19 documentos textuais, 4 imagens e resultados esperados separados. Dataset: [amparo-piloto-multimodal-v0](https://us.cloud.langfuse.com/project/cmwtuztw500wjad0d8k6znpmu/datasets/cmwtwu27x01zgad0jyzn7uyfg). As imagens usam mídia nativa do Langfuse. A revisão humana dos rótulos e a confirmação da interface com Samuel continuam pendentes. Nenhum experimento foi executado.

## Conferir o material agora

Na raiz do repositório:

```sh
python3 scripts/validar_piloto_multimodal.py
```

O comando verifica documentos, vínculos e integridade dos quatro arquivos PNG recebidos, mantendo a ausência intencional de foto em FDE-002. As imagens já estão disponíveis com hashes registrados; concluir revisão humana antes do ensaio.

Nenhuma execução de agente ou avaliação de desempenho foi feita. Não houve nova geração de imagens após o pedido para interromper. A imagem gerada anteriormente foi preservada fora do repositório e excluída deste lote.

## Recebimento das imagens — 23/11/2026

As quatro imagens foram copiadas de Downloads para os nomes esperados, na ordem cronológica de geração. Originais preservados. Revisão visual pelo assistente identificou trincas visíveis e qualidade candidata adequada; isso não substitui validação humana dos rótulos. O lote foi posteriormente importado no Langfuse com autorização de Alex. Nenhum push foi realizado.

## Estado atual no Langfuse

Importação conferida pela API: 5 casos. Dataset: [amparo-piloto-multimodal-v0](https://us.cloud.langfuse.com/project/cmwtuztw500wjad0d8k6znpmu/datasets/cmwtwu27x01zgad0jyzn7uyfg). Identificadores de condições padronizados para `CONDICOES` e tipo `condicoes`. Gabaritos continuam pendentes de revisão humana; nenhum experimento do agente foi executado.
