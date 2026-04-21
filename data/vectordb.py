
from data.ingest import Ingest
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_chroma import Chroma
from Config import CHROMA_PERSIST_DIR, KNOWLEDGE_BASE_DIR

class embedding_vectordb_safe():
    """Classe para pegar os documentos vetorizados e inserir em um vectordb"""
    def __init__(self):

        self.docs = None
        self.chunks = None
        self.embeddings = None

    def load_sources(self):
        """carrega fonte de dados para RAG"""

        ingest = Ingest()
        self.docs = ingest.load_rag_sources(KNOWLEDGE_BASE_DIR)

        return self.docs
    
    def spliterdocuments(self):
        """Cria chunks de documentos"""

        spliter = RecursiveCharacterTextSplitter(
            chunk_size = 500,
            chunk_overlap = 50
        )

        self.chunks = spliter.split_documents(self.docs)

        return self.chunks

    def embedding_sources(self):
        """transforma o conteúdo textual em vetores com OpenAI embeddings"""

        self.embeddings = OpenAIEmbeddings(model="text-embedding-3-large")

        return self.embeddings

    def vectordbload(self):
        """Carrega banco vetorial com chunks. Reutiliza o índice se já existir."""
        import os

        if os.path.exists(CHROMA_PERSIST_DIR) and os.listdir(CHROMA_PERSIST_DIR):
            vector_store = Chroma(
                embedding_function=self.embeddings,
                persist_directory=CHROMA_PERSIST_DIR,
                collection_name="dataflow_rag",
            )
        else:
            vector_store = Chroma.from_documents(
                documents=self.chunks,
                embedding=self.embeddings,
                persist_directory=CHROMA_PERSIST_DIR,
                collection_name="dataflow_rag",
                collection_metadata={"hnsw:space": "cosine"},
            )

        return vector_store
