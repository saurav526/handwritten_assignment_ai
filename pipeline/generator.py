from config import OPENAI_API_KEY, OPENAI_MODEL

SYSTEM_PROMPT = """
You are an academic assignment document assistant.

Given OCR text from handwritten pages:
1. Identify the subject and assignment title when possible.
2. Identify every question and preserve its numbering.
3. Correct obvious OCR errors using context.
4. Preserve the student's intended meaning.
5. Complete incomplete answers.
6. Do not invent questions that are not present.
7. Write clear university-level answers.
8. Use headings, numbering, bullets, tables, and equations when appropriate.
9. If a word is genuinely uncertain, use [unclear] instead of silently inventing it.
10. Return a clean, ready-to-edit assignment.
"""

def generate_assignment(text: str) -> str:
    if not OPENAI_API_KEY:
        raise RuntimeError(
            "OPENAI_API_KEY is missing. Add it to the .env file."
        )

    from openai import OpenAI
    client = OpenAI(api_key=OPENAI_API_KEY)

    response = client.responses.create(
        model=OPENAI_MODEL,
        instructions=SYSTEM_PROMPT,
        input=f"Handwritten assignment transcription:\n\n{text}"
    )

    return response.output_text
