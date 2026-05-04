from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional, Literal
from services.fal_client import generate_image_fal
from services.stability_client import generate_image_stability

router = APIRouter(prefix="/generate-2d", tags=["2D Generation"])


class Generate2DRequest(BaseModel):
    prompt: str
    negative_prompt: Optional[str] = ""
    width: Optional[int] = 1024
    height: Optional[int] = 1024
    provider: Optional[Literal["fal", "stability"]] = "fal"
    style_preset: Optional[str] = None


@router.post("")
async def generate_2d(request: Generate2DRequest):
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