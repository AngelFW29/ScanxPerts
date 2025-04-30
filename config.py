# config.py
import os
import sys

OCR_CONFIG = "--psm 6"


def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS  # Para el ejecutable
    except Exception:
        base_path = os.path.abspath(".")  # Para desarrollo
    return os.path.join(base_path, relative_path)


TESSERACT_CMD = resource_path("Tesseract-OCR/tesseract.exe")  
