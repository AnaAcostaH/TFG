import re
import unidecode

def limpiar_nombre_producto(nombre):
    nombre = nombre.lower()
    nombre = nombre.strip()
    nombre = re.sub(r'\s+', ' ', nombre)  # reemplaza si hay varios espacios por uno
    nombre = unidecode.unidecode(nombre)  # quita tildes y caracteres especiales
    return nombre


def limpiar_precio(precio_raw):
    """
    Extrae solo el valor numérico del precio, ignorando etiquetas como 'precio', saltos de línea, símbolos, etc.
    """
    if not precio_raw:
        return None

    precio_raw = precio_raw.lower()
    precio_raw = re.sub(r'precio', '', precio_raw)        # quita la palabra 'precio'
    precio_raw = re.sub(r'\s+', ' ', precio_raw).strip()  # quita saltos de línea y dobles espacios

    match = re.search(r'(\d+[,.]?\d*)', precio_raw)
    if match:
        return match.group(1).replace(',', '.')
    return None