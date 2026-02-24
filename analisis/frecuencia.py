import pandas as pd


def access_frequency(df: pd.DataFrame, freq: str = "D") -> pd.DataFrame:
    """
    Calculates access frequency per user grouped by time window.

    Parameters:
        df (pd.DataFrame): canonical dataframe
        freq (str): Pandas time frequency ('D'=day, 'W'=week, 'M'=month)

    Returns:
        pd.DataFrame
    """

    df = df.copy()

    # Ensure datetime
    df["event_time"] = pd.to_datetime(df["event_time"])

    # Set as index
    df = df.set_index("event_time")

    # Group by user + time window
    result = (
        df.groupby("actor_name").resample(freq).size().reset_index(name="access_count")
    )

    return result
