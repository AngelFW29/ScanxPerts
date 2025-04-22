def clean_number(value):
    try:
        return f"{float(value.replace(',', '')):.2f}"
    except ValueError:
        return "0.00"


def correct_ncf_format(ncf):
    return (
        ncf.replace("o", "0")
        .replace("O", "0")
        .replace("Bo1", "B01")
        .replace("BO1", "B01")
        .replace("B0I", "B01")
        .replace("BOI", "B01")
        .replace("B0l", "B01")
        .replace("801", "B01")
        .replace("B01", "B01")
    )


def correct_extracted_text(text):
    corrections = {
        "RENTENGIONES": "RETENCIONES",
        "RENTENCIONES": "RETENCIONES",
        "RETENGIONES": "RETENCIONES",
        "SUBTOTALES|": "SUBTOTALES",
        "¢": "$",
        "!": "|",
        "§": "$",
        "‘$": "$",
    }
    for wrong, right in corrections.items():
        text = text.replace(wrong, right)
    return text
