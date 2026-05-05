import httpx
import asyncio
from utils.image_utils import bytes_to_base64, base64_to_bytes

SPACES = [
    "https://stabilityai-triposr.hf.space",
    "https://tencentarc-instantmesh.hf.space",
    "https://jiawei011-dreamgaussian.hf.space",
]


async def _wake_space(client: httpx.AsyncClient, base_url: str):
    """Ping the space to wake it up."""
    try:
        await client.get(f"{base_url}/", timeout=10)
    except Exception:
        pass


async def _try_triposr(image_bytes: bytes, base_url: str) -> dict:
    async with httpx.AsyncClient(timeout=30) as client:
        # Wake up
        await _wake_space(client, base_url)
        await asyncio.sleep(3)

        # Upload
        upload_res = await client.post(
            f"{base_url}/upload",
            files={"files": ("input.png", image_bytes, "image/png")},
            timeout=30,
        )
        upload_res.raise_for_status()
        uploaded_path = upload_res.json()[0]

    payload = {
        "fn_index": 1,
        "data": [
            {"path": uploaded_path, "meta": {"_type": "gradio.FileData"}},
            0.85,
            True,
        ],
        "session_hash": "studio_free",
    }

    async with httpx.AsyncClient(timeout=180) as client:
        res = await client.post(
            f"{base_url}/api/predict",
            json=payload,
            headers={"Content-Type": "application/json"},
        )
        res.raise_for_status()
        result = res.json()

    glb_data = result["data"][0]
    glb_path = glb_data.get("path") or glb_data.get("name")
    return {
        "model_url": f"{base_url}/file={glb_path}",
        "model_format": "glb",
        "provider": base_url,
    }


async def generate_3d_triposr(image_base64: str = None, prompt: str = None) -> dict:
    """
    Tries TripoSR with up to 3 retries + 15s wait between attempts.
    HF Spaces need time to wake from sleep — this handles it automatically.
    """
    image_bytes = base64_to_bytes(image_base64) if image_base64 else None

    # If text-only, generate a placeholder message
    if image_bytes is None:
        raise Exception("image_base64 is required for 3D generation")

    last_error = None
    for attempt in range(3):
        try:
            return await _try_triposr(image_bytes, SPACES[0])
        except Exception as e:
            last_error = e
            wait = 15 * (attempt + 1)
            await asyncio.sleep(wait)

    raise Exception(
        f"TripoSR HF Space unavailable after 3 attempts. "
        f"Last error: {str(last_error)[:120]}. "
        f"The free Space may be under heavy load — try again in a few minutes."
    )