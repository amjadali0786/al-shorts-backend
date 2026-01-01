import os
from PyPDF2 import PdfReader
from PIL import Image
import pytesseract
import docx


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
            if page.extract_text():
                text += page.extract_text() + "\n"
        return text.strip()

    # -------------------------
    # IMAGE (OCR)
    # -------------------------
    if ext in [".png", ".jpg", ".jpeg", ".webp"]:
        img = Image.open(file_path)
        return pytesseract.image_to_string(img, lang="eng+hin").strip()

    # -------------------------
    # DOCX
    # -------------------------
    if ext == ".docx":
        doc = docx.Document(file_path)
        return "\n".join(p.text for p in doc.paragraphs).strip()

    return ""
