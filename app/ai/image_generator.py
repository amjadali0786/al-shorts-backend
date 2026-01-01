import os
import uuid
from groq import Groq

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

IMAGE_DIR = "static/images"
os.makedirs(IMAGE_DIR, exist_ok=True)

def generate_image(image_prompt: str) -> str | None:
    if not image_prompt:
        return None

    try:
        # 🔥 Groq image (example placeholder)
        # Groq does not yet generate images → so we simulate safe placeholder
        filename = f"{uuid.uuid4()}.jpg"
        filepath = os.path.join(IMAGE_DIR, filename)

        # 🧪 TEMP: placeholder image
        with open(filepath, "wb") as f:
            f.write(b"")  # empty image placeholder

        return f"/static/images/{filename}"

    except Exception as e:
        print("❌ IMAGE GEN ERROR:", e)
        return None
