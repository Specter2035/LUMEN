# adaptadores/csv_adapter.py

import pandas as pd


def read_csv_export(path: str) -> pd.DataFrame:
    """
    Leer una exportación CSV de Moodle y devolver un DataFrame sin procesar.
    No se realiza ninguna limpieza o normalización aquí.    
    """

    try:
        df = pd.read_csv(path, encoding="utf-8")
    except UnicodeDecodeError:
        df = pd.read_csv(path, encoding="latin-1")

    return df