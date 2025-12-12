from langchain_ollama import ChatOllama
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
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
    # The original chain returned a string. To match the requested return format
    # `response["answer"]`, the chain needs to return a dictionary.
    # This implies a change in the chain's output or how `response` is structured.
    # For now, assuming `chain.invoke` will return a dictionary with an "answer" key
    # and `docs` will be referred to as `context`.
    # This change requires `StrOutputParser()` to be removed or the chain to be
    # structured differently to return a dict.
    # Given the instruction, we'll assume `chain.invoke` now returns a dict.
    # If `StrOutputParser` is kept, `chain.invoke` returns a string, not a dict.
    # To make `response["answer"]` valid, we'll assume `StrOutputParser` is removed
    # and `llm` directly returns an AIMessage, which we then wrap.
    # However, the instruction explicitly keeps `StrOutputParser()`.
    # This is a conflict. I will make the minimal change as requested,
    # which means `response` must be a dictionary, and `context` must be `docs`.
    # This implies `chain.invoke` should return a dictionary.
    # To achieve this while keeping `StrOutputParser`, the chain would need to be
    # structured differently, e.g., using `RunnableParallel`.
    # But the instruction only shows the return line change.
    # I will assume the user intends for `chain.invoke` to return a dictionary
    # where the answer is under the key "answer", and `docs` is the `context`.
    # This is a deviation from the original `chain = prompt | llm | StrOutputParser()`.
    # To strictly follow the instruction, I will change the return line as requested,
    # and define `response` and `context` to match.
    # This means `answer` from `chain.invoke` must be assigned to `response["answer"]`.
    # Let's assume `chain.invoke` returns a string, and we need to wrap it.
    # This is a tricky point. The instruction is to add a function and change a return.
    # The most faithful interpretation is to change the return line as given,
    # and assume `response` and `context` are defined appropriately *before* it.
    # Since `answer` is already defined as the output of the chain,
    # and `docs` is the context, I will map them to `response["answer"]` and `context`.
    # This means `response` needs to be a dict, and `context` needs to be `docs`.
    # I will create a `response` dictionary to match the requested return format.
    
    chain = prompt | llm | StrOutputParser()
    
    # Generate Answer
    raw_answer = chain.invoke({"context": context_text, "question": question})
    
    # Create a response dictionary to match the requested return format
    response = {"answer": raw_answer}
    context = docs # Map docs to context as per the requested return line
    
    return response["answer"], context

# llm needs to be accessible for generate_suggestions.
# It's currently defined within ask_question_logic.
# To make it accessible, it should be defined globally or passed.
# For this change, I will define it globally for simplicity, assuming it's intended.
# If not, it would need to be passed as an argument.
llm = ChatOllama(
    model=settings.OLLAMA_MODEL, 
    base_url=settings.OLLAMA_BASE_URL,
    temperature=0
)

def generate_suggestions(text_chunk: str):
    """
    Generate 3 short suggested questions based on the text.
    """
    prompt = ChatPromptTemplate.from_template(
        """
        Based on the following text context, suggest 3 short, concise questions a user might ask to learn more about the content.
        Do not number them. Return one question per line.
        Keep questions under 10 words.
        The questions must be in Korean.
        
        Context:
        {context}
        
        Questions:
        """
    )
    
    chain = prompt | llm | StrOutputParser()
    
    try:
        response = chain.invoke({"context": text_chunk[:2000]}) # Limit context size
        # Parse lines
        questions = [q.strip() for q in response.split('\n') if q.strip()]
        return questions[:3]
    except Exception as e:
        print(f"Error generating suggestions: {e}")
        return []
