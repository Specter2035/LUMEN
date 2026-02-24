# adaptadores/normalize.py

import pandas as pd
from datetime import datetime
import hashlib


RAW_TO_STD = {
    "Hora": "event_time",
    "Nombre completo del usuario": "actor_name",
    "Usuario afectado": "affected_user_name",
    "Contexto del evento": "context_raw",
    "Componente": "component",
    "Nombre del evento": "event_name",
    "Descripción": "description_raw",
    "Origen": "origin",
    "Dirección IP": "ip_address",
}

STD_COLUMNS = list(RAW_TO_STD.values())


def normalize_events(
    df: pd.DataFrame, source_file: str, source_format: str
) -> pd.DataFrame:
    """
    Transforma logs de DataFrames de moodle a un esquema canónico
    """

    df = df.copy()
    # 0) Normalizar strings de encabezado (para prevenir discrepancias por espacios)
    df.columns = [str(c).strip() for c in df.columns]

    # 1) Renombrar columnas
    df = df.rename(columns=RAW_TO_STD)

    # 2) Asegurar que columnas canónicas existen (prevenir errores de tipo KeyError si el método renombre no coincide)
    for col in STD_COLUMNS:
        if col not in df.columns:
            df[col] = pd.NA

    # 3) Mantener solo columnas canónicas (ordenadas)
    df = df[STD_COLUMNS]

    # 4) Convertir event_time a datetime
    df["event_time"] = pd.to_datetime(
        df["event_time"],
        format="%d/%m/%y, %H:%M:%S",
        errors="coerce",
    )

    if df["event_time"].isna().any():
        raise ValueError("Datetime parsing failed: event_time contains NaT values.")

    # 5) Reemplazar "-" con None
    df["affected_user_name"] = df["affected_user_name"].replace("-", None)

    # 6) Añadir metadatos
    df["source_file"] = source_file
    df["source_format"] = source_format
    df["ingested_at"] = datetime.utcnow()

    # 7) Crear fila hash para deduplicación
    df["row_hash"] = df.apply(
        lambda row: hashlib.md5(str(row.values).encode()).hexdigest(), axis=1
    )

    return df
