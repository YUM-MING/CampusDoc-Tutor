from langchain_ollama import OllamaEmbeddings
from src.core.config import settings

def get_embeddings():
    return OllamaEmbeddings(
        model=settings.OLLAMA_MODEL,
        base_url=settings.OLLAMA_BASE_URL
    )
