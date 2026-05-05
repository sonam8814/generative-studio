from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional, Literal
from services.fal_client import (
    generate_image_fal,
    sketch_to_image_fal,
    remove_background_fal,
)
from services.stability_client import generate_image_stability

router = APIRouter(prefix="/generate-2d", tags=["2D Generation"])


# ─── Request Models ───────────────────────────────────────────────────────────

class Generate2DRequest(BaseModel):
    prompt: str
    negative_prompt: Optional[str] = ""
    width: Optional[int] = 1024
    height: Optional[int] = 1024
    provider: Optional[Literal["fal", "stability"]] = "fal"
    style_preset: Optional[str] = None


class SketchToImageRequest(BaseModel):
    prompt: str
    image_base64: str                        # PNG sketch from canvas
    strength: Optional[float] = 0.9         # how much to follow the sketch
    guidance_scale: Optional[float] = 7.5


class RemoveBackgroundRequest(BaseModel):
    image_base64: str                        # any PNG/JPG


# ─── Endpoints ────────────────────────────────────────────────────────────────

@router.post("")
async def generate_2d(request: Generate2DRequest):
    """Standard text-to-image via Fal.ai (FLUX) or Stability AI."""
    try:
        if request.provider == "fal":
            result = await generate_image_fal(
                prompt=request.prompt,
                width=request.width,
                height=request.height,
            )
        else:
            result = await generate_image_stability(
                prompt=request.prompt,
                negative_prompt=request.negative_prompt,
                style_preset=request.style_preset,
            )
        return {"status": "success", "provider": request.provider, **result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/sketch-to-image")
async def sketch_to_image(request: SketchToImageRequest):
    """
    ControlNet scribble pipeline.
    Accepts a base64 sketch drawn on the frontend canvas,
    returns a fully rendered image.
    """
    try:
        result = await sketch_to_image_fal(
            prompt=request.prompt,
            image_base64=request.image_base64,
            guidance_scale=request.guidance_scale,
        )
        return {"status": "success", **result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/remove-background")
async def remove_background(request: RemoveBackgroundRequest):
    """
    Background removal via Fal.ai rembg.
    Returns a transparent-background PNG as base64.
    """
    try:
        result = await remove_background_fal(
            image_base64=request.image_base64
        )
        return {"status": "success", **result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/sketch-then-remove-bg")
async def sketch_then_remove_bg(request: SketchToImageRequest):
    """
    Chained pipeline: sketch → rendered image → background removed.
    One call, two API hops.
    """
    try:
        # Step 1: sketch → image
        rendered = await sketch_to_image_fal(
            prompt=request.prompt,
            image_base64=request.image_base64,
            guidance_scale=request.guidance_scale,
        )
        # Step 2: rendered image → transparent PNG
        cleaned = await remove_background_fal(
            image_base64=rendered["image_base64"]
        )
        return {
            "status": "success",
            "rendered_image_base64": rendered["image_base64"],
            "rendered_image_url": rendered["image_url"],
            "final_image_base64": cleaned["image_base64"],
            "final_image_url": cleaned["image_url"],
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))