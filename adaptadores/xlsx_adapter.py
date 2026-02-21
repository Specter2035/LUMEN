# adaptadores/xlsx_adapter.py

import pandas as pd


def read_xlsx_export(path: str) -> pd.DataFrame:
    """
    Reads a Moodle XLSX export and returns a raw DataFrame.
    Assumes data is in the first sheet.
    """

    df = pd.read_excel(path)

    return df