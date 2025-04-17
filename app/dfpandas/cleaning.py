import re
import yaml
import pandas as pd
import logging
import os

logger = logging.getLogger(__name__)

# Ruta basada en la ubicación de este script
base_dir = os.path.dirname(os.path.abspath(__file__))
yaml_path = os.path.join(base_dir, 'config.yaml')


def clean_dataframe(df: pd.DataFrame) -> pd.DataFrame:
    """
    Elimina filas con valores faltantes y mensajes de sistema definidos en un YAML.

    Parameters
    ----------
    df : pd.DataFrame
        DataFrame de entrada, debe contener al menos la columna 'message'.

    Returns
    -------
    pd.DataFrame
        Nuevo DataFrame sin filas con NaN y sin los mensajes de sistema.

    Raises
    ------
    FileNotFoundError
        Si no existe el archivo de configuración.
    yaml.YAMLError
        Si el YAML no se puede parsear correctamente.
    Exception
        Para cualquier otro error durante el proceso.
    """
    try:
        df = df.copy()
        before = len(df)

        # 1) Drop filas con cualquier NaN
        df.dropna(inplace=True)
        logger.debug("dropna: %d → %d filas", before, len(df))

        # 2) Cargar configuración
        try:
            with open(yaml_path, encoding="utf-8") as f:
                config_yaml = yaml.safe_load(f)
            logger.debug("Configuración cargada desde '%s'", yaml_path)
        except FileNotFoundError:
            logger.error("No se encontró el archivo de configuración: %s", yaml_path)
            raise FileNotFoundError(f"Archivo de configuración no encontrado: {yaml_path}")
        except yaml.YAMLError as e:
            logger.error("Error al parsear YAML '%s': %s", yaml_path, e)
            raise yaml.YAMLError(f"Error al parsear YAML: {e}")

        # 3) Construir lista de patrones
        skip_dict = config_yaml.get("skip_messages", {})
        patterns = []
        for key, entry in skip_dict.items():
            if isinstance(entry, dict):
                patterns.extend(entry.values())
            else:
                logger.warning("Formato inesperado en la entrada '%s': %r", key, entry)

        if not patterns:
            logger.info("No hay patrones definidos en 'skip_messages'; se omite filtrado.")
            return df.reset_index(drop=True)

        escaped = [re.escape(p) for p in patterns]
        regex = r"(?:" + "|".join(escaped) + r")"

        # 4) Filtrar mensajes
        mask = df["message"].str.contains(regex, case=False, na=False, regex=True)
        df_filtered = df[~mask].reset_index(drop=True)
        logger.info("Filtrado mensajes de sistema: %d → %d filas", len(df), len(df_filtered))

        return df_filtered

    except Exception as e:
        logger.exception("Error en clean_dataframe: %s", e)
        raise
