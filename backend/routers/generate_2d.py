from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional
from services.pollinations_client import generate_image_pollinations
from services.hf_client import sketch_to_image_hf
from services.rembg_client import remove_background_local

router = APIRouter(prefix="/generate-2d", tags=["2D Generation"])


class Generate2DRequest(BaseModel):
    prompt: str
    width: Optional[int] = 1024
    height: Optional[int] = 1024
    model: Optional[str] = "flux"


class SketchToImageRequest(BaseModel):
    prompt: str
    image_base64: str
    guidance_scale: Optional[float] = 7.5


class RemoveBackgroundRequest(BaseModel):
    image_base64: str


@router.post("")
async def generate_2d(request: Generate2DRequest):
    """Text → image via Pollinations.ai (free, no key)."""
    try:
        result = await generate_image_pollinations(
            prompt=request.prompt,
            width=request.width,
            height=request.height,
            model=request.model,
        )
        return {"status": "success", **result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/sketch-to-image")
async def sketch_to_image(request: SketchToImageRequest):
    """Sketch PNG → rendered image via HF ControlNet."""
    try:
        result = await sketch_to_image_hf(
            prompt=request.prompt,
            image_base64=request.image_base64,
            guidance_scale=request.guidance_scale,
        )
        return {"status": "success", **result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/remove-background")
async def remove_background(request: RemoveBackgroundRequest):
    """Background removal via rembg (local, free, no API call)."""
    try:
        result = remove_background_local(request.image_base64)
        return {"status": "success", **result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/sketch-then-remove-bg")
async def sketch_then_remove_bg(request: SketchToImageRequest):
    """Chained: sketch → rendered image → background removed."""
    try:
        rendered = await sketch_to_image_hf(
            prompt=request.prompt,
            image_base64=request.image_base64,
            guidance_scale=request.guidance_scale,
        )
        cleaned = remove_background_local(rendered["image_base64"])
        return {
            "status": "success",
            "rendered_image_base64": rendered["image_base64"],
            "final_image_base64": cleaned["image_base64"],
            "provider": "hf+rembg",
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))