# Handwritten Assignment AI

A Streamlit application that accepts handwritten assignment images, preprocesses them, extracts text with OCR, uses an LLM to analyze/complete the assignment, and exports the result as DOCX.

## Pipeline

Image → OpenCV preprocessing → PaddleOCR → editable OCR text → LLM analysis/generation → DOCX

## 1. Create environment

### Windows

```powershell
python -m venv .venv
.venv\Scripts\activate
```

### macOS/Linux

```bash
python3 -m venv .venv
source .venv/bin/activate
```

## 2. Install

```bash
pip install -r requirements.txt
```

> PaddlePaddle installation can vary by CPU/GPU and operating system. If the standard `pip install -r requirements.txt` fails specifically on PaddlePaddle, install the compatible PaddlePaddle build for your machine first, then rerun the requirements installation without changing the application code.

## 3. Configure API key

Copy `.env.example` to `.env` and set:

```env
OPENAI_API_KEY=your_key
OPENAI_MODEL=gpt-5.6-mini
```

## 4. Run

```bash
streamlit run app.py
```

## 5. How to use

1. Upload one or multiple handwritten pages.
2. Click **Analyze Assignment**.
3. Review/correct OCR text.
4. Click **Generate Complete Assignment**.
5. Edit the final result if necessary.
6. Download the DOCX.

## Notes

- OCR quality depends heavily on handwriting, image quality, language, and page layout.
- The current OCR stage is a baseline. For difficult handwriting, add a dedicated handwriting recognizer such as TrOCR and/or a vision-language fallback.
- The generator is intentionally separated from OCR so the LLM provider can be replaced later.
- For high-stakes academic use, review generated content for correctness before submission.

## Recommended future upgrades

- TrOCR line-level handwriting recognition
- Page layout detection
- Equation recognition
- Diagram recognition
- RAG over class notes/textbooks
- PDF export
- User accounts and assignment history
- OCR confidence scoring
- Fine-tuning on a custom handwriting dataset
