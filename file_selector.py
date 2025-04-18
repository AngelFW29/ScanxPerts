import tkinter as tk
from tkinter import filedialog


def seleccionar_imagen():
    """Abre un cuadro de diálogo para seleccionar un archivo de imagen."""
    root = tk.Tk()
    root.withdraw()  # Ocultar la ventana principal

    archivo = filedialog.askopenfilename(
        title="Selecciona una imagen",
        filetypes=[("Archivos de imagen", "*.jpg;*.jpeg;*.png;*.bmp")],
    )

    return archivo if archivo else None  # Retorna None en lugar de lanzar un error
