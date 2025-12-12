from langchain_ollama import ChatOllama
from langchain_core.output_parsers import StrOutputParser
from src.rag.vectorstore import get_vectorstore
from src.rag.prompts import get_qa_prompt
from src.core.config import settings
from typing import Tuple, List
from langchain_core.documents import Document

def ask_question_logic(question: str) -> Tuple[str, List[Document]]:
    vectorstore = get_vectorstore()
    # Retrieve top 3 documents
    retriever = vectorstore.as_retriever(search_kwargs={"k": 3})
    docs = retriever.invoke(question)
    
    # Format context
    context_text = "\n\n".join([d.page_content for d in docs])
    
    # Setup LLM Chain - Switched to Ollama
    llm = ChatOllama(
        model=settings.OLLAMA_MODEL, 
        base_url=settings.OLLAMA_BASE_URL,
        temperature=0
    )
    prompt = get_qa_prompt()
    chain = prompt | llm | StrOutputParser()
    
    # Generate Answer
    answer = chain.invoke({"context": context_text, "question": question})
    
    return answer, docs
