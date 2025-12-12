from langchain_core.documents import Document
from src.api.schemas import Citation
from typing import List
import os

def format_citations(documents: List[Document]) -> List[Citation]:
    citations = []
    for doc in documents:
        source_path = doc.metadata.get("source", "unknown")
        # Extract just the filename for cleaner display
        filename = os.path.basename(source_path)
        page = doc.metadata.get("page", 0) + 1  # 0-indexed to 1-indexed
        
        # Taking a snippet of content
        content_snippet = doc.page_content[:150].replace("\n", " ") + "..."
        
        citations.append(Citation(
            content=content_snippet,
            source=filename,
            page=page
        ))
    return citations
