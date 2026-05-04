from dotenv import load_dotenv
import os

load_dotenv()

FAL_KEY = os.getenv("FAL_KEY")
STABILITY_KEY = os.getenv("STABILITY_KEY")

# Fal.ai model endpoints
FAL_IMAGE_MODEL    = "fal-ai/flux/schnell"          # fast text-to-image
FAL_CONTROLNET     = "fal-ai/controlnet-scribble"   # sketch-to-image
FAL_3D_MODEL       = "fal-ai/triposr"               # image-to-3D
FAL_REMBG_MODEL    = "fal-ai/imageutils/rembg"      # background removal

# Stability AI
STABILITY_API_URL  = "https://api.stability.ai/v2beta/stable-image/generate/core"