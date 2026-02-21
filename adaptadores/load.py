# adaptadores/load.py

import os
from adaptadores.csv_adapter import read_csv_export
from adaptadores.xlsx_adapter import read_xlsx_export
from adaptadores.normalize import normalize_events


def load_events(path: str):
    """
    Automáticamente detecta el tipo de archivo y devuelve un DataFrame canónico.    
    """

    extension = os.path.splitext(path)[1].lower()

    if extension == ".csv":
        raw_df = read_csv_export(path)
        format_type = "csv"

    elif extension == ".xlsx":
        raw_df = read_xlsx_export(path)
        format_type = "xlsx"

    else:
        raise ValueError(f"Unsupported format: {extension}")

    canonical_df = normalize_events(
        raw_df,
        source_file=os.path.basename(path),
        source_format=format_type
    )

    return canonical_df