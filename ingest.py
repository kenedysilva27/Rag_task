from langchain_community.document_loaders import PyPDFDirectoryLoader
from langchain_chroma import Chroma

class Ingest():
    """Módulo para buscar os documentos para Rag,aplicar embeddings e colocar no vectordb"""

    def __init__(self,loader,docs):
        self.loader = loader
        self.docs = docs

    def load_rag_sources(self,past):
        """carrega arquivos dentro de uma pasta especifica"""
        self.loader = PyPDFDirectoryLoader(past)

        self.docs = self.loader.load()

        return self.docs
    
    def embedding_sources(self):
        """transforma o conteúdo textual em vetores com openia embeddigns"""
        self.vectorstore = Chroma()
