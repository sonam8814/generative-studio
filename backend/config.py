from dotenv import load_dotenv
import os

load_dotenv()

HF_TOKEN = os.getenv("HF_TOKEN", "")  # free HF token — only needed for ControlNet

# ── 2D: Pollinations.ai (no key, no auth) ─────────────────────────────────────
POLLINATIONS_URL = "https://image.pollinations.ai/prompt/{prompt}"

# ── Sketch-to-Image: HF Inference API ─────────────────────────────────────────
HF_CONTROLNET_URL = (
    "https://api-inference.huggingface.co/models/"
    "lllyasviel/sd-controlnet-scribble"
)

# ── Background Removal: rembg (local, ~50MB, no GPU) ──────────────────────────
# No URL needed — runs in-process

# ── 3D: HF Space TripoSR (free public space, no key) ──────────────────────────
TRIPOSR_SPACE_URL = "https://stabilityai-triposr.hf.space"