import httpx
import asyncio
import json
from utils.image_utils import bytes_to_base64, base64_to_bytes

# Free public HF Space — no key needed
TRIPOSR_PREDICT_URL = "https://stabilityai-triposr.hf.space/api/predict"


async def generate_3d_triposr(image_base64: str) -> dict:
    """
    Calls the free public TripoSR HF Space via Gradio API.
    Pipeline: base64 image → upload → run → poll → return .GLB URL
    """
    image_bytes = base64_to_bytes(image_base64)

    # Step 1: Upload image to the Space
    upload_url = "https://stabilityai-triposr.hf.space/upload"
    async with httpx.AsyncClient(timeout=60) as client:
        upload_response = await client.post(
            upload_url,
            files={"files": ("input.png", image_bytes, "image/png")},
        )
        upload_response.raise_for_status()
        uploaded_path = upload_response.json()[0]  # server-side temp path

    # Step 2: Run prediction
    payload = {
        "fn_index": 1,           # TripoSR main inference function
        "data": [
            {"path": uploaded_path, "meta": {"_type": "gradio.FileData"}},
            0.85,                # foreground_ratio
            True,                # do_remove_background
        ],
        "session_hash": "studio_session",
    }

    async with httpx.AsyncClient(timeout=180) as client:
        predict_response = await client.post(
            TRIPOSR_PREDICT_URL,
            json=payload,
            headers={"Content-Type": "application/json"},
        )
        predict_response.raise_for_status()
        result = predict_response.json()

    # Step 3: Extract GLB path
    glb_data = result["data"][0]
    glb_path = glb_data.get("path") or glb_data.get("name")
    glb_url = f"https://stabilityai-triposr.hf.space/file={glb_path}"

    return {
        "model_url": glb_url,
        "model_format": "glb",
        "provider": "triposr-hf-space",
    }