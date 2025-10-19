# ocr.py
import pytesseract
from PIL import Image
import pyautogui

# Optional: set tesseract path on macOS
pytesseract.pytesseract.tesseract_cmd = "/opt/homebrew/bin/tesseract"

def capture_screenshot(region=None):
    """
    Capture a screenshot.
    region: (left, top, width, height) or None for full screen
    """
    screenshot = pyautogui.screenshot(region=region)
    return screenshot

def extract_text_from_image(image):
    """Convert PIL image to text using OCR"""
    text = pytesseract.image_to_string(image)
    return text

def capture_and_extract(region=None):
    """Capture screenshot and extract text in one step"""
    image = capture_screenshot(region)
    text = extract_text_from_image(image)
    return text
