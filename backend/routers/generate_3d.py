from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional
from services.fal_client import generate_3d_fal, generate_image_fal
from utils.image_utils import url_to_base64

router = APIRouter(prefix="/generate-3d", tags=["3D Generation"])


class Generate3DFromImageRequest(BaseModel):
    image_base64: str  # client sends a base64 PNG


class Generate3DFromTextRequest(BaseModel):
    prompt: str        # text → image (Fal FLUX) → 3D (TripoSR)


@router.post("/from-image")
async def generate_3d_from_image(request: Generate3DFromImageRequest):
    try:
        result = await generate_3d_fal(image_base64=request.image_base64)
        return {"status": "success", **result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/from-text")
async def generate_3d_from_text(request: Generate3DFromTextRequest):
    """Two-step pipeline: text → 2D image → 3D model."""
    try:
        image_result = await generate_image_fal(
            prompt=request.prompt, width=1024, height=1024
        )
        model_result = await generate_3d_fal(
            image_base64=image_result["image_base64"]
        )
        return {
            "status": "success",
            "intermediate_image_url": image_result["image_url"],
            **model_result,
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))