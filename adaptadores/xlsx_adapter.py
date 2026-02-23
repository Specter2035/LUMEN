# adaptadores/xlsx_adapter.py

import pandas as pd


def read_xlsx_export(path: str) -> pd.DataFrame:
    """
    Lee un exportación XLSX de Moodle y devuelve un DataFrame sin procesar.
    Asume que los datos están en la primera hoja.
    """

    df = pd.read_excel(path)

    return df