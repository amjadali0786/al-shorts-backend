import os
from groq import Groq

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def summarize_text(text: str) -> dict:
    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
messages = [
    {
        "role": "system",
        "content": (
            "You are a professional news editor specializing in Inshorts-style news summaries.\n\n"
            "ABSOLUTE RULES ((STRICT AND MANDATORY NO EXCEPTIONS):\n"
            "1. Use ONLY the information explicitly provided by the user.\n"
            "2. Do NOT add assumptions, background context, opinions, or external facts.\n"
            "3. Do NOT change, expand, or shift the topic in any way.\n"
            "4. Summaries MUST be factual, neutral, and written in a professional journalistic tone.\n"
            "5. Each summary MUST contain AT LEAST 50 words. Outputs below 50 words are INVALID.\n"
            "6. Do NOT use filler, repetition, or artificial padding to reach the word limit.\n"
            "7. Titles must be concise, clear, and strictly news-focused.\n"
            "8. Language must be simple, realistic, and suitable for a mobile news app.\n\n"

            "IMAGE PROMPT GENERATION RULES (STRICT AND MANDATORY):\n"
            "• The image_prompt MUST be generated dynamically based on the news content.\n"
            "• The image_prompt MUST be a SINGLE sentence written as a direct command.\n"
            "• It MUST start EXACTLY with: \"Generate a picture of\".\n"
            "• The image_prompt MUST describe a real-world visual scene implied by the news.\n"
            "• The image MUST look like a realistic, editorial news photograph.\n"
            "• The image_prompt MUST explicitly state that the image is composed for a FIXED 1:1 square frame.\n"
            "• The image_prompt MUST explicitly include the size \"1024x1024\".\n"
            "• Avoid strong emotional direction (e.g., crying, angry, terrified).\n"
            "• Do NOT use words such as: describe, showing, with, caption, text overlay, written text.\n"
            "• Do NOT mention illustrations, drawings, artistic styles, or cinematic effects.\n"
            "• Visual elements MUST be strictly limited to what is implied by the content.\n\n"

            "FAILURE CONDITION:\n"
            "• If the provided content is insufficient to produce a minimum 50-word summary without adding facts, still produce the summary using ONLY the available information.\n\n"

            "OUTPUT FORMAT (MANDATORY):\n"
            "• Respond ONLY in valid JSON.\n"
            "• Do NOT include explanations, markdown, comments, or extra text.\n"
            "• Follow the EXACT structure below:\n\n"
            "{\n"
            "  \"title_hi\": \"\",\n"
            "  \"summary_hi\": \"\",\n"
            "  \"title_en\": \"\",\n"
            "  \"summary_en\": \"\",\n"
            "  \"image_prompt\": \"\"\n"
            "}"
        )
    },
    {
        "role": "user",
        "content": text
    }
]

,
        temperature=0.1
    )

    return eval(response.choices[0].message.content)
