from fastapi import APIRouter, HTTPException
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from typing import Optional
import httpx

from services.triposr_client import generate_3d_triposr
from services.pollinations_client import generate_image_pollinations

router = APIRouter(prefix="/generate-3d", tags=["3D Generation"])


# ─── Request Models ───────────────────────────────────────────────────────────

class Generate3DFromImageRequest(BaseModel):
    image_base64: str


class Generate3DFromTextRequest(BaseModel):
    prompt: str
    width: Optional[int] = 1024
    height: Optional[int] = 1024


# ─── Endpoints ────────────────────────────────────────────────────────────────

@router.post("/from-image")
async def generate_3d_from_image(request: Generate3DFromImageRequest):
    """Image → .GLB via TripoSR HF Space (free, with wake-up retry)."""
    try:
        result = await generate_3d_triposr(image_base64=request.image_base64)
        return {"status": "success", **result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/from-text")
async def generate_3d_from_text(request: Generate3DFromTextRequest):
    """
    Two-step fully free pipeline:
      1. Text → image via Pollinations.ai (no key, FLUX model)
      2. Image → .GLB via TripoSR HF Space (free, with wake-up retry)
    """
    try:
        # Step 1: text → image
        image_result = await generate_image_pollinations(
            prompt=request.prompt,
            width=request.width,
            height=request.height,
        )

        # Step 2: image → 3D (with automatic wake-up + retry logic)
        model_result = await generate_3d_triposr(
            image_base64=image_result["image_base64"]
        )

        return {
            "status": "success",
            "intermediate_image_base64": image_result["image_base64"],
            "intermediate_image_url": image_result["image_url"],
            **model_result,
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/download")
async def download_model(url: str, filename: Optional[str] = "model.glb"):
    """
    Proxy-download endpoint — streams .GLB/.OBJ to browser.
    Avoids CORS issues with direct HF Space CDN URLs.
    Usage: GET /generate-3d/download?url=<glb_url>&filename=model.glb
    """
    try:
        async with httpx.AsyncClient(timeout=120) as client:
            response = await client.get(url, follow_redirects=True)
            response.raise_for_status()

        fmt = filename.split(".")[-1].lower()
        content_type_map = {
            "glb":  "model/gltf-binary",
            "obj":  "text/plain",
            "mtl":  "text/plain",
            "gltf": "model/gltf+json",
        }
        content_type = content_type_map.get(fmt, "application/octet-stream")

        return StreamingResponse(
            content=iter([response.content]),
            media_type=content_type,
            headers={
                "Content-Disposition": f'attachment; filename="{filename}"',
                "Content-Length": str(len(response.content)),
            },
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))