import httpx
from config import STABILITY_KEY, STABILITY_API_URL
from utils.image_utils import bytes_to_base64


async def generate_image_stability(
    prompt: str,
    negative_prompt: str = "",
    aspect_ratio: str = "1:1",
    style_preset: str = None,
) -> dict:
    """Text-to-image via Stability AI Core."""
    headers = {
        "Authorization": f"Bearer {STABILITY_KEY}",
        "Accept": "image/*",
    }
    data = {
        "prompt": prompt,
        "aspect_ratio": aspect_ratio,
        "output_format": "png",
    }
    if negative_prompt:
        data["negative_prompt"] = negative_prompt
    if style_preset:
        data["style_preset"] = style_preset

    async with httpx.AsyncClient(timeout=60) as client:
        response = await client.post(STABILITY_API_URL, headers=headers, data=data)
        response.raise_for_status()
        return {
            "image_base64": bytes_to_base64(response.content),
            "finish_reason": response.headers.get("finish-reason", "SUCCESS"),
            "seed": response.headers.get("seed"),
        }