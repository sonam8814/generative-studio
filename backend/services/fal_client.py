import fal_client
import httpx
import os
from config import (
    FAL_KEY,
    FAL_IMAGE_MODEL,
    FAL_CONTROLNET,
    FAL_3D_MODEL,
    FAL_REMBG_MODEL,
)
from utils.image_utils import url_to_base64

os.environ["FAL_KEY"] = FAL_KEY
os.environ["FAL_API_KEY"] = FAL_KEY


# ─── Text-to-Image ────────────────────────────────────────────────────────────

async def generate_image_fal(
    prompt: str,
    width: int = 1024,
    height: int = 1024,
) -> dict:
    """FLUX Schnell: fast text-to-image."""
    result = await fal_client.run_async(
        FAL_IMAGE_MODEL,
        arguments={
            "prompt": prompt,
            "image_size": {"width": width, "height": height},
            "num_inference_steps": 4,
            "num_images": 1,
        },
    )
    image_url = result["images"][0]["url"]
    return {
        "image_base64": url_to_base64(image_url),
        "image_url": image_url,
        "seed": result.get("seed"),
    }


# ─── Sketch-to-Image (ControlNet) ─────────────────────────────────────────────

async def sketch_to_image_fal(
    prompt: str,
    image_base64: str,
    guidance_scale: float = 7.5,
) -> dict:
    """
    ControlNet scribble: turns a rough sketch into a rendered image.
    The base64 PNG is sent as a data URI — no separate upload needed.
    """
    image_data_uri = f"data:image/png;base64,{image_base64}"
    result = await fal_client.run_async(
        FAL_CONTROLNET,
        arguments={
            "prompt": prompt,
            "image_url": image_data_uri,
            "num_inference_steps": 25,
            "guidance_scale": guidance_scale,
            "controlnet_conditioning_scale": 0.9,
        },
    )
    image_url = result["images"][0]["url"]
    return {
        "image_base64": url_to_base64(image_url),
        "image_url": image_url,
    }


# ─── Background Removal ───────────────────────────────────────────────────────

async def remove_background_fal(image_base64: str) -> dict:
    """
    Fal.ai rembg: removes background, returns transparent PNG.
    """
    image_data_uri = f"data:image/png;base64,{image_base64}"
    result = await fal_client.run_async(
        FAL_REMBG_MODEL,
        arguments={"image_url": image_data_uri},
    )
    image_url = result["image"]["url"]
    return {
        "image_base64": url_to_base64(image_url),
        "image_url": image_url,
    }


# ─── Image-to-3D ──────────────────────────────────────────────────────────────

async def generate_3d_fal(image_base64: str) -> dict:
    """TripoSR: single image → .GLB 3D model."""
    image_data_uri = f"data:image/png;base64,{image_base64}"
    result = await fal_client.run_async(
        FAL_3D_MODEL,
        arguments={
            "image_url": image_data_uri,
            "do_remove_background": True,
            "foreground_ratio": 0.85,
            "output_format": "glb",
        },
    )
    return {
        "model_url": result["model_mesh"]["url"],
        "model_format": "glb",
    }