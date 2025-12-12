from fastapi import FastAPI
from src.api.routes import router

from fastapi.staticfiles import StaticFiles
import os

app = FastAPI(title="CampusDoc Tutor", description="RAG based tutor")

# Ensure static directory exists
static_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "static")
os.makedirs(static_dir, exist_ok=True)

app.include_router(router)

# Serve raw PDF files for preview
# MUST be mounted before the root static files to avoid masking
raw_data_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "..", "data", "raw")
# Ensure it exists effectively for the mount, even if empty initially
os.makedirs(raw_data_dir, exist_ok=True)
app.mount("/raw_files", StaticFiles(directory=raw_data_dir), name="raw_files")

app.mount("/", StaticFiles(directory=static_dir, html=True), name="static")
