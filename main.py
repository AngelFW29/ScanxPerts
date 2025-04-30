# main
import customtkinter as ctk
import tkinter as tk
from tkinter import filedialog, messagebox
from ocr_extractor import process_invoice
from file_selector import seleccionar_imagen
from pdf_to_image import pdf_to_images
from excel_writer import (
    write_data_to_excel,
    guardar_en_nuevo_excel,
    guardar_en_excel_existente,
)


class ToolTip:
    def __init__(self, widget, text):
        self.widget = widget
        self.text = text
        self.tooltip = None
        widget.bind("<Enter>", self.show_tooltip)
        widget.bind("<Leave>", self.hide_tooltip)

    def show_tooltip(self, event=None):
        x = y = 0
        x = self.widget.winfo_pointerx() + 10
        y = self.widget.winfo_pointery() + 10

        self.tooltip = tk.Toplevel(self.widget)
        self.tooltip.wm_overrideredirect(True)
        self.tooltip.wm_geometry(f"+{x}+{y}")

        label = tk.Label(
            self.tooltip,
            text=self.text,
            background="#333",
            foreground="white",
            relief="solid",
            borderwidth=1,
            padx=5,
            pady=2,
            font=("Segoe UI", 10),
        )
        label.pack()

    def hide_tooltip(self, event=None):
        if self.tooltip:
            self.tooltip.destroy()
            self.tooltip = None


# Inicializar tema y modo
ctk.set_appearance_mode("dark")  #  "light" o "system"
ctk.set_default_color_theme("blue")  # "green", "dark-blue"

# Variable para almacenar los datos de la factura procesada
invoice_data = {}


# Función para manejar el evento de seleccionar archivo y procesar la imagen
def seleccionar_y_procesar_archivo():
    try:
        # Usamos file_selector para abrir el cuadro de diálogo y seleccionar el archivo
        archivo = seleccionar_imagen()

        # Si el usuario cancela la selección, mostrar advertencia y salir de la función
        if not archivo:
            messagebox.showwarning("Aviso", "No se seleccionó ningún archivo.")
            return

        # Si el archivo es PDF, convertirlo a imágenes
        if archivo.endswith(".pdf"):
            imagenes = pdf_to_images(archivo)
            for imagen in imagenes:
                global invoice_data
                invoice_data = process_invoice(
                    imagen
                )  # Procesamos cada imagen convertida desde el PDF
                # Mostrar los resultados en el área de texto
                mostrar_resultados(invoice_data)
        elif archivo.endswith((".png", ".jpg", ".jpeg")):
            # Si el archivo es una imagen, procesarlo directamente
            invoice_data = process_invoice(archivo)
            # Mostrar los resultados en el área de texto
            mostrar_resultados(invoice_data)
        else:
            messagebox.showwarning(
                "Aviso",
                "Formato de archivo no compatible. Usa PDF o imagen (.jpg, .png).",
            )
    except Exception as e:
        messagebox.showerror("Error", f"Ocurrió un error al procesar el archivo: {e}")


# Función para mostrar los resultados en el área de texto
def mostrar_resultados(invoice_data):
    resultado_texto.configure(state="normal")  # Habilitar edición temporalmente
    resultado_texto.delete(1.0, tk.END)  # Limpiar texto anterior
    for key, value in invoice_data.items():
        resultado_texto.insert(tk.END, f"{key}: {value}\n")
    resultado_texto.configure(state="disabled")  # Deshabilitar edición


# Función para guardar los datos en Excel
def guardar_en_excel():
    try:
        if not invoice_data:
            messagebox.showwarning("Aviso", "No hay datos para guardar.")
            return
        write_data_to_excel(invoice_data)
        messagebox.showinfo("Éxito", "Los datos han sido guardados en el Excel.")
        limpiar_pantalla()
        invoice_data.clear()
    except Exception as e:
        messagebox.showerror("Error", f"Ocurrió un error al guardar los datos: {e}")


# Función para convertir PDF a imagen
def convertir_pdf_a_imagen():
    archivo_pdf = filedialog.askopenfilename(
        title="Seleccionar archivo PDF",
        filetypes=[("Archivos PDF", "*.pdf")],
    )

    if not archivo_pdf:
        messagebox.showwarning("Aviso", "No se seleccionó ningún archivo.")
        return

    try:
        # Seleccionar carpeta donde guardar las imágenes
        carpeta_destino = filedialog.askdirectory(
            title="Selecciona la carpeta para guardar las imágenes"
        )

        if not carpeta_destino:
            messagebox.showwarning(
                "Aviso", "No se seleccionó ninguna carpeta para guardar las imágenes."
            )
            return

        imagenes = pdf_to_images(archivo_pdf)
        messagebox.showinfo(
            "Éxito",
            f"Se convirtieron {len(imagenes)} página(s) y se guardaron en la ruta seleccionada.",
        )
    except Exception as e:
        messagebox.showerror("Error", f"Ocurrió un error: {e}")


def seleccionar_opcion_guardado():
    ventana_opciones = ctk.CTkToplevel()
    ventana_opciones.title("Seleccionar tipo de guardado")
    ventana_opciones.geometry("400x180")
    ventana_opciones.grab_set()  # Bloquea la ventana principal

    etiqueta = ctk.CTkLabel(
        ventana_opciones,
        text="¿Dónde deseas guardar los datos?",
        font=("Segoe UI", 16),
    )
    etiqueta.pack(pady=20)

    def guardar_nuevo_excel():
        ventana_opciones.destroy()
        if invoice_data:
            guardar_en_nuevo_excel(invoice_data)
            limpiar_pantalla()
            invoice_data.clear()
        else:
            messagebox.showwarning("Aviso", "No hay datos para guardar.")

    def guardar_excel_existente():
        ventana_opciones.destroy()
        if invoice_data:
            guardar_en_excel_existente(invoice_data)
            limpiar_pantalla()
            invoice_data.clear()
        else:
            messagebox.showwarning("Aviso", "No hay datos para guardar.")

    boton_nuevo = ctk.CTkButton(
        ventana_opciones,
        text="Guardar en nuevo Excel",
        command=guardar_nuevo_excel,
        width=200,
    )
    boton_nuevo.pack(pady=5)

    boton_existente = ctk.CTkButton(
        ventana_opciones,
        text="Guardar en Excel existente",
        command=guardar_excel_existente,
        width=200,
    )
    boton_existente.pack(pady=5)


# Limpiar pantalla
def limpiar_pantalla():
    resultado_texto.configure(state="normal")
    resultado_texto.delete(1.0, tk.END)
    resultado_texto.configure(state="disabled")


# ---------------------- INTERFAZ ------------------------
ventana = ctk.CTk()
ventana.title("ScanXperts")
ventana.geometry("800x550")
ventana.resizable(False, False)

# Título principal
ctk.CTkLabel(ventana, text="Procesador de Facturas", font=("Segoe UI", 26)).pack(
    pady=20
)

# Frame para botones
frame_botones = ctk.CTkFrame(ventana)
frame_botones.pack(pady=10)

boton_convertir_pdf = ctk.CTkButton(
    frame_botones,
    text="Convertir PDF a Imagen",
    command=convertir_pdf_a_imagen,
    width=200,
)
boton_convertir_pdf.grid(row=0, column=0, padx=10, pady=5)

boton_seleccionar_imagen = ctk.CTkButton(
    frame_botones,
    text="Seleccionar Imagen",
    command=seleccionar_y_procesar_archivo,
    width=200,
)
boton_seleccionar_imagen.grid(row=0, column=1, padx=10, pady=5)

boton_guardar_excel = ctk.CTkButton(
    frame_botones,
    text="Guardar en Excel",
    command=seleccionar_opcion_guardado,
    width=200,
)
boton_guardar_excel.grid(row=0, column=2, padx=10, pady=5)

# Añadir ToolTips a los botones
ToolTip(boton_convertir_pdf, "Convierte un archivo PDF en imágenes.")
ToolTip(boton_seleccionar_imagen, "Seleccione una imagen o archivo PDF de factura.")
ToolTip(boton_guardar_excel, "Elija dónde desea guardar los datos extraídos.")

# Frame para resultados con scrollbar
frame_resultado = ctk.CTkFrame(ventana)
frame_resultado.pack(pady=20, fill="both", expand=True)

resultado_texto = ctk.CTkTextbox(
    frame_resultado, width=740, height=300, font=("Consolas", 20)
)
resultado_texto.pack(side="left", fill="both", expand=True, padx=10, pady=10)
resultado_texto.configure(state="disabled")

ventana.mainloop()
