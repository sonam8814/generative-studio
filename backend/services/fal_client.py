import fal_client as fal
import httpx
from config import FAL_KEY, FAL_IMAGE_MODEL, FAL_CONTROLNET, FAL_3D_MODEL, FAL_REMBG_MODEL
from utils.image_utils import url_to_base64
import os

os.environ["FAL_KEY"] = FAL_KEY
os.environ["FAL_API_KEY"] = FAL_KEY


async def generate_image_fal(prompt: str, width: int = 1024, height: int = 1024) -> dict:
    """Text-to-image via Fal.ai FLUX Schnell."""
    result = await fal.run_async(
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


async def sketch_to_image_fal(prompt: str, image_base64: str) -> dict:
    """ControlNet scribble: sketch-to-image via Fal.ai."""
    image_data_uri = f"data:image/png;base64,{image_base64}"
    result = await fal.run_async(
        FAL_CONTROLNET,
        arguments={
            "prompt": prompt,
            "image_url": image_data_uri,
            "num_inference_steps": 20,
            "guidance_scale": 7.5,
        },
    )
    image_url = result["images"][0]["url"]
    return {
        "image_base64": url_to_base64(image_url),
        "image_url": image_url,
    }


async def remove_background_fal(image_base64: str) -> dict:
    """Background removal via Fal.ai rembg."""
    image_data_uri = f"data:image/png;base64,{image_base64}"
    result = await fal.run_async(
        FAL_REMBG_MODEL,
        arguments={"image_url": image_data_uri},
    )
    image_url = result["image"]["url"]
    return {"image_base64": url_to_base64(image_url), "image_url": image_url}


async def generate_3d_fal(image_base64: str) -> dict:
    """Image-to-3D via Fal.ai TripoSR — returns .GLB URL."""
    image_data_uri = f"data:image/png;base64,{image_base64}"
    result = await fal.run_async(
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