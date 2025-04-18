import cv2
import pytesseract
import re
from datetime import datetime
from data_formatter import clean_number, correct_ncf_format, correct_extracted_text
from config import TESSERACT_CMD, OCR_CONFIG

pytesseract.pytesseract_cmd = TESSERACT_CMD


def extract_value(pattern, text, default=""):
    matches = re.findall(pattern, text)
    return matches[-1] if matches else default


def process_invoice(image_path):
    image = cv2.imread(image_path)
    if image is None:
        raise FileNotFoundError(f"No se pudo cargar la imagen: {image_path}")

    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    extracted_text = pytesseract.image_to_string(gray, config=OCR_CONFIG)
    extracted_text = correct_extracted_text(extracted_text)

    # Prueba
    print("Texto OCR EXTRAIDO\n", extracted_text)

    rnc_pattern = r"RNC:\s*(\d+)"
    ncf_pattern = r"NCF\s*(?:de N\. de D\.)?:?\s*(B\d{2}\d+|\bBO1\d+)"
    ncf_mod_pattern = r"NCF:\s*Modificada\s*(B[Oo0I1]{2}\d+)"
    fecha_pattern = r"FECHA:\s*(\d{2}/\d{2}/\d{4})"
    monto_pattern = r"SUBTOTAL[\s\]]*\s*\$\s*([\d,]+\.\d+)"
    itbis_pattern = r"ITBIS\s*\(\d+%\)[\)\}]*\s*\$\s*([\d,]+\.\d+)"
    retencion_pattern = r"RETENCIONES\s*\(?\d*%?\)?\s*[:|!]*\s*[\$\¢]?\s*([\d,]+\.\d+)"

    rnc_cliente = extract_value(rnc_pattern, extracted_text)
    ncf = correct_ncf_format(extract_value(ncf_pattern, extracted_text))
    ncf_modificado = correct_ncf_format(
        extract_value(ncf_mod_pattern, extracted_text, "")
    )
    fecha_comprobante = extract_value(fecha_pattern, extracted_text)

    # Tomar la primera fecha
    fechas = re.findall(fecha_pattern, extracted_text)
    if fechas:
        if ncf.startswith("B03"):
            # Si es una factura B03, tomamos la primera fecha
            fecha_comprobante = datetime.strptime(fechas[0], "%d/%m/%Y").strftime(
                "%Y%m%d"
            )
        else:
            # Para las demás facturas, usamos la última fecha (en el caso de B01 o cualquier otro)
            fecha_comprobante = datetime.strptime(fechas[-1], "%d/%m/%Y").strftime(
                "%Y%m%d"
            )
    else:
        fecha_comprobante = "00000000"

    monto_facturado = clean_number(extract_value(monto_pattern, extracted_text))
    itbis_facturado = clean_number(extract_value(itbis_pattern, extracted_text))
    retencion = clean_number(extract_value(retencion_pattern, extracted_text))

    if (ncf.startswith("B03") or ncf.startswith("B04")) and not ncf_modificado:
        ncf_modificado = correct_ncf_format(
            extract_value(r"B[Oo0I1]{2}\d+", extracted_text, "")
        )

    cheque_transferencia_deposito = (
        f"{float(monto_facturado) + float(itbis_facturado):.2f}"
    )

    return {
        "RNC/Cédula o Pasaporte": rnc_cliente,
        "Tipo Identificación": 1,
        "Número Comprobante Fiscal": ncf,
        "Número Comprobante Fiscal Modificado": ncf_modificado,
        "Tipo de Ingreso": "01 - Ingresos por Operaciones (No Financieros)",
        "Fecha Comprobante": fecha_comprobante,
        "Fecha de Retención": fecha_comprobante,
        "Monto Facturado": monto_facturado,
        "ITBIS Facturado": itbis_facturado,
        "ITBIS Retenido por Terceros": retencion,
        "Cheque/ Transferencia/ Depósito": cheque_transferencia_deposito,
    }
