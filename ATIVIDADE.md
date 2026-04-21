# Atividade Final — RAG Avançado

## Contexto

Você é engenheiro de IA da **DataFlow Analytics**, empresa de dados fundada em 2021 em Campinas-SP.
A empresa quer um **chatbot interno** que responda perguntas dos colaboradores sobre produtos, políticas de RH e documentação técnica da API.

Os documentos da empresa já existem na pasta `base_conhecimento/` em formato PDF.

O sistema deve ser uma **aplicação Python modular**.

---

## O que você deve entregar

### 1. Ingestão de documentos — `ingest.py`

Um módulo que:
- Carrega os PDFs da pasta `base_conhecimento/`
- Enriquece cada chunk com metadados que serão persistidos no vector store:
  - `source`: nome do arquivo de origem (ex: `produtos.pdf`)
  - `categoria`: domínio do documento — `comercial`, `rh` ou `tecnico`
- Divide o conteúdo em partes menores prontas para indexação

Esses metadados ficam gravados junto ao vetor no Chroma e podem ser usados pelo retriever para filtrar por categoria durante a busca.

---

### 2. Busca — `retriever.py`

Um módulo que:
- Indexa os trechos em um vector store com persistência em disco
- Reutiliza o índice já criado sem reprocessar tudo
- Realiza busca híbrida: combinando busca por similaridade semântica e busca por palavras-chave
- Aplica reranking nos resultados para priorizar os mais relevantes

---

### 3. Chain conversacional — `chain.py`

Um módulo que:
- Recebe uma pergunta e retorna uma resposta baseada nos documentos
- Mantém histórico da conversa para entender perguntas de acompanhamento (ex: *"e o preço dele?"*)
- Responde apenas com base no conteúdo dos documentos — nunca inventa informação

---

### 4. API REST — `api.py`

Um módulo que expõe o chatbot como uma API HTTP para integração com outros sistemas.

Deve conter os seguintes endpoints:

| Método | Rota | Descrição |
|--------|------|-----------|
| `POST` | `/chat` | Recebe uma pergunta e retorna a resposta do RAG |
| `GET` | `/health` | Retorna o status da API |
| `DELETE` | `/session/{session_id}` | Encerra o histórico de uma sessão |

O endpoint `/chat` deve suportar `session_id` para que cada usuário tenha seu próprio histórico de conversa.

---

### 5. Avaliação — `evaluation.py`

Um módulo que:
- Carrega o arquivo `golden_set.json` com perguntas e respostas esperadas
- Executa o RAG para cada pergunta
- Calcula métricas de qualidade e exibe os resultados no terminal

---

### 6. Aplicação principal — `main.py`

Um arquivo de entrada que:
- Carrega variáveis de ambiente de um `.env`
- Monta o pipeline completo
- Inicia um chat interativo no terminal onde o histórico é mantido durante a sessão
- Encerra quando o usuário digitar `sair`

---

## Critérios de avaliação

| Módulo | O que será verificado |
|--------|----------------------|
| `ingest.py` | PDFs carregados; metadados `source` e `categoria` presentes e persistidos no vector store para todos os chunks |
| `retriever.py` | Busca híbrida funcionando; reranking aplicado; índice persistido e reutilizado |
| `chain.py` | Perguntas de acompanhamento resolvidas corretamente; respostas só com base no contexto |
| `api.py` | Endpoints funcionando; histórico separado por `session_id` |
| `evaluation.py` | Métricas calculadas e exibidas para todas as perguntas do golden set |
| `main.py` | Chat funcional no terminal com histórico mantido durante a sessão |
