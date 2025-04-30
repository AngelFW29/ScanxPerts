# config.py
import os
import sys

OCR_CONFIG = "--psm 6"


def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS  # Al ejecutar el .exe
    except Exception:
        base_path = os.path.abspath(".")  # Al ejecutar como script
    return os.path.join(base_path, relative_path)


# TESSERACT_CMD = resource_path("tesseract/tesseract.exe")
TESSERACT_CMD = resource_path("resource/Tesseract-OCR/tesseract.exe")
