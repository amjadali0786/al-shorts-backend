from app.core.database import SessionLocal
from app.models.news import News
from app.ai.summarizer import summarize_text

def process_content(content):
    print("🟡 AI PIPELINE STARTED")

    text = content.text_content
    if not text or not text.strip():
        print("🔴 No text found")
        return

    # -------------------------
    # AI CALL
    # -------------------------
    ai_output = summarize_text(text)

    print("🧪 DEBUG AI RAW OUTPUT:")
    print(ai_output)

    # -------------------------
    # SAFE EXTRACTION
    # -------------------------
    title_hi = ai_output.get("title_hi")
    summary_hi = ai_output.get("summary_hi")
    title_en = ai_output.get("title_en")
    summary_en = ai_output.get("summary_en")
    image_prompt = ai_output.get("image_prompt")

    # -------------------------
    # DB SAVE
    # -------------------------
    db = SessionLocal()
    try:
        news = News(
            title_hi=title_hi,
            summary_hi=summary_hi,
            title_en=title_en,
            summary_en=summary_en,
            image_prompt=image_prompt,
            image_url=None,
            status="draft",
        )

        db.add(news)
        db.commit()
        db.refresh(news)

        print(f"✅ NEWS SAVED | ID = {news.id}")

    except Exception as e:
        db.rollback()
        print("❌ DB ERROR:", e)

    finally:
        db.close()
