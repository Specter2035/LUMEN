# adaptadores/csv_adapter.py

import pandas as pd


def read_csv_export(path: str) -> pd.DataFrame:
    """
    Reads a Moodle CSV export and returns a raw DataFrame.
    No cleaning or normalization is performed here.
    """

    try:
        df = pd.read_csv(path, encoding="utf-8")
    except UnicodeDecodeError:
        df = pd.read_csv(path, encoding="latin-1")

    return df