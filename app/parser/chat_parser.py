import re
import pandas as pd
import logging
from app.parser.patterns import PATTERN_APPLE, PATTERN_ANDROID

logger = logging.getLogger(__name__)

def extract_line(line: str):
    """
    Extrae la fecha, hora, usuario y mensaje de una línea del chat.

    Parameters:
        line (str): Línea del archivo de chat.

    Returns:
        tuple: (date_str, time_str, user, message) si la extracción es exitosa;
        de lo contrario, (None, None, None, None).
    """
    pattern = PATTERN_APPLE if line.startswith('[') else PATTERN_ANDROID
    match = re.search(pattern, line)
    if match:
        return (
            match.group("date"),
            match.group("time"),
            match.group("user"),
            match.group("message")
        )
    return None, None, None, None

def parse_datetime(date_str: str, time_str: str) -> pd.Timestamp:
    """
    Convierte cadenas de fecha y hora en un objeto datetime de pandas.

    Parameters:
        date_str (str): Fecha en formato dd/mm/yy o dd/mm/yyyy.
        time_str (str): Hora que puede incluir segundos y/o indicadores AM/PM.

    Returns:
        datetime: Objeto datetime parseado.

    Raises:
        ValueError: Si no se puede parsear la fecha y hora.
    """
    clean_time = re.sub(r'\.', '', time_str)
    clean_time = " ".join(clean_time.split())
    # Busca y reemplaza separadamente patrones de "a m" por "am"  insensible a mayúsculas/minúsculas
    clean_time = re.sub(r'(?i)\b([ap])\s+([m])\b', r'\1\2', clean_time)
    # Determina si la cadena de tiempo contiene el indicador AM/PM.
    has_ampm = re.search(r'\b(?:am|pm)\b', clean_time, re.IGNORECASE)
    has_seconds = clean_time.count(':') == 2 # Determina si se han incluido segundos contando ":"
    short_year = len(date_str.split('/')[-1]) == 2 # Verifica si el año se expresa en dos dígitos.

    if has_ampm: # Para formato 12 horas
        date_format = "%d/%m/%y" if short_year else "%d/%m/%Y"
        time_format = " %I:%M:%S %p" if has_seconds else " %I:%M %p"
    else: # Para formato 24 horas
        date_format = "%d/%m/%y" if short_year else "%d/%m/%Y"
        time_format = " %H:%M:%S" if has_seconds else " %H:%M"

    # Se compone el formato completo
    dt_format = date_format + time_format
    date_time_str = f"{date_str} {clean_time}"

    #intenta convertir a datime
    try:
        dt = pd.to_datetime(date_time_str, format=dt_format)
    except Exception as e:
        logger.error(
            "Error parseando datetime para '%s' usando el formato '%s': %s",
            date_time_str, dt_format, e
        )
        raise ValueError(f"Error parseando datetime: {e}")
    return dt