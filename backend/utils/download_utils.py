import httpx
import os
from pathlib import Path

DOWNLOADS_DIR = Path(__file__).parent.parent / "downloads"
DOWNLOADS_DIR.mkdir(exist_ok=True)


async def fetch_and_save_model(url: str, filename: str) -> Path:
    """
    Downloads a 3D model from a URL and saves it locally.
    Returns the local file path.
    """
    dest = DOWNLOADS_DIR / filename
    async with httpx.AsyncClient(timeout=120) as client:
        response = await client.get(url)
        response.raise_for_status()
        dest.write_bytes(response.content)
    return dest


def list_saved_models() -> list[dict]:
    """Returns metadata of all locally saved models."""
    models = []
    for f in DOWNLOADS_DIR.iterdir():
        if f.suffix in {".glb", ".obj", ".gltf"}:
            models.append({
                "filename": f.name,
                "size_kb": round(f.stat().st_size / 1024, 2),
                "format": f.suffix.lstrip("."),
            })
    return models