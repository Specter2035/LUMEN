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


def normalize_events(df: pd.DataFrame, source_file: str, source_format: str) -> pd.DataFrame:
    """
    Transforms raw Moodle log DataFrame into canonical schema.
    """

    # Rename columns
    df = df.rename(columns=RAW_TO_STD)

    # Keep only canonical columns
    df = df[list(RAW_TO_STD.values())]

    # Convert event_time to datetime
    df["event_time"] = pd.to_datetime(
    df["event_time"],
    format="%Y-%m-%d %H:%M:%S",
    errors="coerce"
    )

    # Replace "-" with None
    df["affected_user_name"] = df["affected_user_name"].replace("-", None)

    # Add metadata
    df["source_file"] = source_file
    df["source_format"] = source_format
    df["ingested_at"] = datetime.utcnow()

    # Create row hash for deduplication
    df["row_hash"] = df.apply(
        lambda row: hashlib.md5(str(row.values).encode()).hexdigest(),
        axis=1
    )

    return df