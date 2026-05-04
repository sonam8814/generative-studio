import base64
import httpx
from PIL import Image
from io import BytesIO


def url_to_base64(image_url: str) -> str:
    """Fetch a remote image URL and return as base64 string."""
    response = httpx.get(image_url, timeout=30)
    response.raise_for_status()
    encoded = base64.b64encode(response.content).decode("utf-8")
    return encoded


def bytes_to_base64(image_bytes: bytes) -> str:
    """Convert raw bytes to base64 string."""
    return base64.b64encode(image_bytes).decode("utf-8")


def base64_to_bytes(b64_string: str) -> bytes:
    """Decode a base64 string back to bytes."""
    return base64.b64decode(b64_string)


def resize_image_bytes(image_bytes: bytes, max_size: int = 1024) -> bytes:
    """Resize image to max_size on longest edge, returns bytes."""
    img = Image.open(BytesIO(image_bytes)).convert("RGB")
    img.thumbnail((max_size, max_size), Image.LANCZOS)
    buffer = BytesIO()
    img.save(buffer, format="PNG")
    return buffer.getvalue()