from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import generate_2d, generate_3d
from utils.download_utils import list_saved_models

app = FastAPI(
    title="Generative Studio API",
    description="API-first 2D/3D generation — no local model loading.",
    version="2.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(generate_2d.router)
app.include_router(generate_3d.router)


@app.get("/health")
async def health():
    return {"status": "ok", "version": "2.0.0"}


@app.get("/models")
async def list_models():
    """Lists all 3D models saved server-side."""
    return {"models": list_saved_models()}