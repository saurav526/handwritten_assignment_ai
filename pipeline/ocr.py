import os

_OCR = None

def _load_ocr():
    global _OCR
    if _OCR is None:
        from paddleocr import PaddleOCR
        _OCR = PaddleOCR(lang="en")
    return _OCR

def extract_text(image_path: str) -> str:
    """
    OCR wrapper. PaddleOCR versions differ in their result API, so this
    function handles the common predict() structure and falls back cleanly.
    """
    ocr = _load_ocr()
    result = ocr.predict(image_path)

    texts = []

    for page in result:
        if isinstance(page, dict) and "rec_texts" in page:
            texts.extend([str(x) for x in page["rec_texts"]])
        elif hasattr(page, "get"):
            vals = page.get("rec_texts")
            if vals:
                texts.extend([str(x) for x in vals])

    return "\n".join(texts)
