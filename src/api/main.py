from fastapi import FastAPI
from src.api.routes import router

app = FastAPI(title="CampusDoc Tutor", description="RAG based tutor")

app.include_router(router)
