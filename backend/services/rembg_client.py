from rembg import remove
from PIL import Image
from io import BytesIO
from utils.image_utils import bytes_to_base64, base64_to_bytes


def remove_background_local(image_base64: str) -> dict:
    """
    Removes background using rembg (local, ~50MB ONNX model).
    No API call — runs fully in-process.
    Returns transparent PNG as base64.
    """
    image_bytes = base64_to_bytes(image_base64)
    input_image = Image.open(BytesIO(image_bytes)).convert("RGBA")

    output_image = remove(input_image)

    buffer = BytesIO()
    output_image.save(buffer, format="PNG")
    result_bytes = buffer.getvalue()

    return {
        "image_base64": bytes_to_base64(result_bytes),
        "image_url": None,
        "provider": "rembg-local",
    }