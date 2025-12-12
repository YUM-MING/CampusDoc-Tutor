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
        
        # Generate suggestions from the first chunk
        from src.rag.chain import generate_suggestions
        suggestions = []
        if chunks:
            suggestions = generate_suggestions(chunks[0].page_content)

        return {
            "filename": file.filename, 
            "status": "indexed", 
            "chunks_count": len(chunks),
            "suggestions": suggestions
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

@router.get("/files")
async def list_files():
    files = []
    if os.path.exists(RAW_DATA_DIR):
        for f in os.listdir(RAW_DATA_DIR):
            if f.endswith(".pdf"):
                file_path = os.path.join(RAW_DATA_DIR, f)
                size_bytes = os.path.getsize(file_path)
                # Convert size to readable format
                if size_bytes < 1024:
                    size_str = f"{size_bytes} B"
                elif size_bytes < 1024 * 1024:
                    size_str = f"{size_bytes / 1024:.1f} KB"
                else:
                    size_str = f"{size_bytes / (1024 * 1024):.1f} MB"
                
                files.append({
                    "name": f,
                    "size": size_str,
                    "url": f"/raw_files/{f}"
                })
    return {"files": files}

@router.delete("/reset")
async def reset_database():
    try:
        # Clear raw files
        if os.path.exists(RAW_DATA_DIR):
            shutil.rmtree(RAW_DATA_DIR)
            os.makedirs(RAW_DATA_DIR, exist_ok=True)
        
        # Clear ChromaDB
        chroma_dir = "data/chroma"
        if os.path.exists(chroma_dir):
            shutil.rmtree(chroma_dir)
            
        return {"status": "success", "message": "Database and files have been reset."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
