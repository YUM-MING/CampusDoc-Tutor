from langchain_core.prompts import ChatPromptTemplate

SYSTEM_PROMPT = """You are a helpful assistant for CampusDoc Tutor.
Answer the user's question based ONLY on the following context.
If the answer is not in the context, say "문서에서 찾을 수 없습니다." and do not invent an answer.

Context:
{context}
"""

def get_qa_prompt():
    return ChatPromptTemplate.from_messages([
        ("system", SYSTEM_PROMPT),
        ("human", "{question}"),
    ])
