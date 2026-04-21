from langchain_community.document_loaders import PyPDFDirectoryLoader
import os

CATEGORY_MAP = {
    "produtos": "comercial",
    "politicas_rh": "rh",
    "documentacao_api": "tecnico",
}

class Ingest():
    """Classe que busca os documentos para RAG e enriquece com metadados"""

    def __init__(self):

        self.docs = None

    def load_rag_sources(self, path):
        """Carrega os PDFs e adiciona metadados de source e categoria em cada chunk"""

        loader = PyPDFDirectoryLoader(path)
        self.docs = loader.load()

        for doc in self.docs:
            filename = os.path.basename(doc.metadata.get("source", ""))
            name_without_ext = os.path.splitext(filename)[0]
            doc.metadata["source"] = filename
            doc.metadata["categoria"] = CATEGORY_MAP.get(name_without_ext, "desconhecido")

        return self.docs


