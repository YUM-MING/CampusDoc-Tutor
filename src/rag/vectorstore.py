from langchain_chroma import Chroma
from src.core.config import settings
from src.rag.embeddings import get_embeddings
from langchain_core.documents import Document
from typing import List

def get_vectorstore():
    embeddings = get_embeddings()
    return Chroma(
        persist_directory=settings.CHROMA_PERSIST_DIRECTORY,
        embedding_function=embeddings
    )

def add_documents_to_vectorstore(documents: List[Document]):
    vectorstore = get_vectorstore()
    vectorstore.add_documents(documents)
    # Chroma validates persistence automatically in recent configurations, 
    # but explicit persist() call is sometimes needed depending on version. 
    # Langchain Community Chroma wrappers usually auto-persist.
