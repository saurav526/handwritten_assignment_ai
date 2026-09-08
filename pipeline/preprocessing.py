import cv2
import numpy as np
from PIL import Image

def preprocess_image(image: Image.Image) -> Image.Image:
    arr = np.array(image.convert("RGB"))
    gray = cv2.cvtColor(arr, cv2.COLOR_RGB2GRAY)

    # Mild denoising while preserving handwriting strokes.
    gray = cv2.GaussianBlur(gray, (3, 3), 0)

    # Improve local contrast.
    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
    gray = clahe.apply(gray)

    # Keep a grayscale image by default; aggressive thresholding can destroy faint handwriting.
    return Image.fromarray(gray)
