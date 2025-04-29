# pdf_to_image.py
from pdf2image import convert_from_path
import os
from tkinter import filedialog, messagebox

# Ruta de Poppler (ajústala si cambia de ubicación)
POPPLER_PATH = r"C:\Users\Usuario\OneDrive\Escritorio\ScanxPerts\resource\bin"


def pdf_to_images(pdf_path, output_folder=None):
    """
    Convierte un PDF en una o más imágenes JPG.

    Args:
        pdf_path (str): Ruta al archivo PDF.
        output_folder (str): Carpeta donde se guardarán las imágenes.

    Returns:
        list: Lista de rutas de las imágenes generadas.
    """
    if output_folder is None:
        output_folder = filedialog.askdirectory(
            title="Seleccionar carpeta para guardar imágenes"
        )
        if not output_folder:
            messagebox.showinfo("Cancelado", "No se seleccionó carpeta de guardado.")
            return []

    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    try:
        images = convert_from_path(pdf_path, poppler_path=POPPLER_PATH)
    except Exception as e:
        print(f"Error al convertir el PDF a imágenes: {e}")
        return []

    image_paths = []
    base_name = os.path.splitext(os.path.basename(pdf_path))[0]

    for i, image in enumerate(images):
        image_name = f"{base_name}_page_{i+1}.jpg"
        image_path = os.path.join(output_folder, image_name)
        image.save(image_path, "JPEG")
        image_paths.append(image_path)

    return image_paths


# Prueba local del módulo (solo para debug, no usar en producción)
# if __name__ == "__main__":
#     pdf_file = "resource/Materiales del Scanner/Facturas - B01.pdf"
#     images = pdf_to_images(pdf_file)
#     if images:
#         print(f"Conversión exitosa: {len(images)} páginas convertidas 🚀")
#     else:
#         print("No se pudo convertir el PDF.")
