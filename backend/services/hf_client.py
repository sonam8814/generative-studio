import httpx
import base64
from config import HF_TOKEN, HF_CONTROLNET_URL
from utils.image_utils import url_to_base64, bytes_to_base64


async def sketch_to_image_hf(
    prompt: str,
    image_base64: str,
    guidance_scale: float = 7.5,
    num_inference_steps: int = 25,
) -> dict:
    """
    HF Inference API — ControlNet scribble.
    Converts a sketch PNG (base64) into a rendered image.
    """
    headers = {"Content-Type": "application/json"}
    if HF_TOKEN:
        headers["Authorization"] = f"Bearer {HF_TOKEN}"

    payload = {
        "inputs": image_base64,
        "parameters": {
            "prompt": prompt,
            "guidance_scale": guidance_scale,
            "num_inference_steps": num_inference_steps,
        },
    }

    async with httpx.AsyncClient(timeout=120) as client:
        response = await client.post(
            HF_CONTROLNET_URL,
            headers=headers,
            json=payload,
        )
        response.raise_for_status()

    return {
        "image_base64": bytes_to_base64(response.content),
        "image_url": None,
        "provider": "huggingface",
    }