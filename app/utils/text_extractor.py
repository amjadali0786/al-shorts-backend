import os
from PyPDF2 import PdfReader
import docx

# -------------------------
# OPTIONAL OCR (SAFE)
# -------------------------
try:
    import pytesseract
except Exception:
    pytesseract = None

from PIL import Image


def extract_text(file_path: str) -> str:
    ext = os.path.splitext(file_path)[1].lower()
    text = ""

    # -------------------------
    # TXT
    # -------------------------
    if ext == ".txt":
        with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
            return f.read().strip()

    # -------------------------
    # PDF
    # -------------------------
    if ext == ".pdf":
        reader = PdfReader(file_path)
        for page in reader.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"
        return text.strip()

    # -------------------------
    # IMAGE (OCR – OPTIONAL)
    # -------------------------
    if ext in [".png", ".jpg", ".jpeg", ".webp"]:
        if pytesseract is None:
            # 🔥 Render-safe: OCR disabled but app continues
            return ""
        try:
            img = Image.open(file_path)
            return pytesseract.image_to_string(img, lang="eng+hin").strip()
        except Exception:
            return ""

    # -------------------------
    # DOCX
    # -------------------------
    if ext == ".docx":
        doc = docx.Document(file_path)
        return "\n".join(p.text for p in doc.paragraphs).strip()

    return ""
