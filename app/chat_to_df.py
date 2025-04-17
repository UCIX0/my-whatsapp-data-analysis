import re
import os
import pandas as pd
import logging
from app.parser.chat_parser import extract_line, parse_datetime
from app.parser.patterns import SYSTEM_PATTERN_ANDROID, SYSTEM_PATTERN_APPLE


logger = logging.getLogger(__name__)

class ChatProcessingError(Exception):
    """Excepción para errores en el procesamiento del chat."""
    pass

def chat_to_dataframe(file_path) -> pd.DataFrame:
    """
    Procesa un archivo de chat en formato texto y retorna su contenido en un DataFrame de pandas.
    Soporta concatenación de líneas para mensajes que abarquen varias líneas.

    Parameters:
        file_path (str): Ruta al archivo de chat.

    Returns:
        DataFrame: DataFrame con columnas ['datetime', 'user', 'message'].

    Raises:
        FileNotFoundError: Si el archivo no existe.
        ChatProcessingError: Para otros errores relacionados con el procesamiento.
    """

    # Verifica si el archivo existe
    if not os.path.exists(file_path):
        error_msg = f"El archivo '{file_path}' no existe."
        logger.error(error_msg)
        raise FileNotFoundError(error_msg)

    records = []
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            for num_line, line in enumerate(file, 1):
                # Eliminamos espacios laterales y caracteres invisibles problemáticos
                line = line.rstrip()
                line = re.sub(r'[\u200B-\u200F\u202A-\u202E\u2060-\u206F\uFEFF]', '', line)

                # Extrae los componentes
                date_str, time_str, user, message = extract_line(line)

                # Si se extrae con exito los componentes (no es None)
                if date_str and time_str and user is not None:
                    try: # Intenta parsear datetime
                        dt = parse_datetime(date_str, time_str)
                    except Exception as e:
                        logger.warning(
                            "Registro %d: error en parseo de datetime; línea omitida. Error: %s",
                            num_line, e
                        )
                        continue # Salta a la siguiente línea
                    #Si todo ok, crea el registro
                    record = {"datetime": dt, "user": user, "message": message}
                    records.append(record)
                else:
                    # Si no se puede extraer, verifica si es un mensaje continuado (NO es mensaje del sistam)
                    if not (re.match(SYSTEM_PATTERN_ANDROID, line) or re.match(SYSTEM_PATTERN_APPLE, line)) and records:
                        records[-1]["message"] += " " + line.strip() # Agrega el mensaje a la última entrada
                    else:
                        logger.debug("Línea %d no coincide con ningún patrón: %s", num_line, line)

    #Error archivo codificado mal o corrupto
    except UnicodeDecodeError as e:
        error_msg = f"Error de decodificación al leer el archivo '{file_path}': {e}"
        logger.error(error_msg)
        raise ChatProcessingError(error_msg) from e
    #Error error del codigo al parsear
    except Exception as e:
        error_msg = f"Se produjo un error durante el procesamiento del archivo: {e}"
        logger.error(error_msg)
        raise ChatProcessingError(error_msg) from e

    df = pd.DataFrame(records, columns=["datetime", "user", "message"])
    #Error Dataframe vacio
    if df.empty:
        error_msg = "El DataFrame resultante está vacío. Verifica el formato y contenido del archivo."
        logger.warning(error_msg)
        raise ChatProcessingError(error_msg)

    return df
