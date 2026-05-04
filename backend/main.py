from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import generate_2d, generate_3d

app = FastAPI(
    title="Generative Studio API",
    description="API-first 2D/3D generation backend — no local model loading.",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # Vite dev server
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(generate_2d.router)
app.include_router(generate_3d.router)


@app.get("/health")
async def health():
    return {"status": "ok", "message": "Generative Studio backend running"}