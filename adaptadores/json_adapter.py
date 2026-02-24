# adaptadores/json_adapter.py

import json
import pandas as pd


JSON_TO_RAW = {
    "hora": "Hora",
    "nombrecompletodelusuario": "Nombre completo del usuario",
    "usuarioafectado": "Usuario afectado",
    "contextodelevento": "Contexto del evento",
    "componente": "Componente",
    "nombredelevento": "Nombre del evento",
    "descripcin": "Descripción",
    "origen": "Origen",
    "direccinip": "Dirección IP",
}


def read_json_export(path: str) -> pd.DataFrame:
    """
    Lee una exportación JSON de Moodle y devuelve un DataFrame sin procesar.
    No se realiza ninguna limpieza o normalización aquí.
    """

    with open(path, "r", encoding="utf-8") as f:
        payload = json.load(f)

    # Case: wrapped in dict
    if isinstance(payload, dict):
        logs = payload.get("logs")

        if isinstance(logs, list):
            # logs may be nested one level
            if logs and isinstance(logs[0], list):
                logs = logs[0]

            if logs and all(isinstance(x, dict) for x in logs):
                df = pd.DataFrame(logs)
                df = df.rename(columns=JSON_TO_RAW)
                return df

        # fallback: treat dict as single record
        df = pd.DataFrame([payload])
        df = df.rename(columns=JSON_TO_RAW)
        return df

    # Case: top-level list
    if isinstance(payload, list):
        if payload and isinstance(payload[0], list):
            payload = payload[0]

        df = pd.DataFrame(payload)
        df = df.rename(columns=JSON_TO_RAW)
        return df

    raise ValueError(f"Unsupported JSON structure in file: {path}")
