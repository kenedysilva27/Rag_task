from data.vectordb import embedding_vectordb_safe
from langchain_community.retrievers import BM25Retriever
from langchain_cohere import CohereRerank
from Config import COHERE_API_KEY


class recover():

    def __init__(self):
        
        self.chunks = None
        self.vector_db = None
        self.retriever = None

    def recoverembedding(self):

        vector_store = embedding_vectordb_safe()
        vector_store.load_sources()
        self.chunks = vector_store.spliterdocuments()
        vector_store.embedding_sources()
        self.vector_db = vector_store.vectordbload()

        return self.vector_db, self.chunks

    def semanticsearch(self):

        self.retriever = self.vector_db.as_retriever(
            search_kwargs={"k": 10}
        )

        return self.retriever

    def bm25search(self, query):

        bm25_retriever = BM25Retriever.from_documents(self.chunks)
        bm25_retriever.k = 10
        docs = bm25_retriever.invoke(query)

        return docs

    def hybridsearch(self, query):

        semantic_docs = self.retriever.invoke(query)
        bm25_docs = self.bm25search(query)

        seen = set()
        combined = []
        for doc in semantic_docs + bm25_docs:
            key = doc.page_content
            if key not in seen:
                seen.add(key)
                combined.append(doc)

        return combined

    def reranker(self, query):

        combined_docs = self.hybridsearch(query)

        cohere_reranker = CohereRerank(
            cohere_api_key=COHERE_API_KEY,
            model="rerank-multilingual-v3.0",
            top_n=5
        )

        reranked_docs = cohere_reranker.compress_documents(combined_docs, query)

        return reranked_docs


if __name__ == "__main__":

    retriever = recover()
    retriever.recoverembedding()
    retriever.semanticsearch()

    query = "Quais são os benefícios dos funcionários?"
    reranked = retriever.reranker(query)

    print(f"Documentos retornados após reranking: {len(reranked)}\n")
    for i, doc in enumerate(reranked):
        print(f"--- Documento {i+1} ---")
        print(f"Fonte: {doc.metadata.get('source', 'desconhecido')}")
        print(f"Categoria: {doc.metadata.get('categoria', 'desconhecido')}")
        print(doc.page_content[:200])
        print()









