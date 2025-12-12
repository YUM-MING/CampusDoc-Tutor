from fastapi import APIRouter, UploadFile, File, HTTPException
from src.api.schemas import AskRequest, AskResponse
from src.rag.loaders import load_pdf
from src.rag.splitter import get_splitter
from src.rag.vectorstore import add_documents_to_vectorstore
from src.rag.chain import ask_question_logic
from src.rag.citations import format_citations
import os
import shutil

router = APIRouter()

RAW_DATA_DIR = "data/raw"
os.makedirs(RAW_DATA_DIR, exist_ok=True)

@router.post("/ingest")
async def ingest_document(file: UploadFile = File(...)):
    if not file.filename.endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only PDF files are supported.")
    
    file_path = os.path.join(RAW_DATA_DIR, file.filename)
    
    try:
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
            
        docs = load_pdf(file_path)
        splitter = get_splitter()
        chunks = splitter.split_documents(docs)
        add_documents_to_vectorstore(chunks)
        
        return {
            "filename": file.filename, 
            "status": "indexed", 
            "chunks_count": len(chunks)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ingestion failed: {str(e)}")

@router.post("/ask", response_model=AskResponse)
async def ask_question(request: AskRequest):
    try:
        answer, docs = ask_question_logic(request.question)
        citations = format_citations(docs)
        return AskResponse(answer=answer, citations=citations)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
