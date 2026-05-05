import httpx
from urllib.parse import quote
from utils.image_utils import bytes_to_base64, resize_image_bytes

POLLINATIONS_BASE = "https://image.pollinations.ai/prompt"


async def generate_image_pollinations(
    prompt: str,
    width: int = 1024,
    height: int = 1024,
    seed: int = None,
    model: str = "flux",        # flux | turbo
    nologo: bool = True,
) -> dict:
    """
    Pollinations.ai — free, no auth, FLUX model.
    Returns base64 PNG + the source URL.
    """
    encoded_prompt = quote(prompt)
    params = {
        "width": width,
        "height": height,
        "model": model,
        "nologo": str(nologo).lower(),
        "nofeed": "true",        # don't publish to public feed
    }
    if seed is not None:
        params["seed"] = seed

    url = f"{POLLINATIONS_BASE}/{encoded_prompt}"

    async with httpx.AsyncClient(timeout=60) as client:
        response = await client.get(url, params=params, follow_redirects=True)
        response.raise_for_status()

    image_bytes = response.content
    # Ensure consistent size
    resized = resize_image_bytes(image_bytes, max_size=max(width, height))

    return {
        "image_base64": bytes_to_base64(resized),
        "image_url": str(response.url),
        "model": model,
        "provider": "pollinations",
    }