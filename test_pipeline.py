import pandas as pd
from adaptadores.load import load_events
from analisis.frecuencia import access_frequency

path = "datos/exports/logs_KX7A_20260220-1944_GrupoB.json"

df = load_events(path)

df["event_time"] = pd.to_datetime(df["event_time"])

start = "2024-11-15"
end = "2024-12-15"

df_range = df[(df["event_time"] >= start) & (df["event_time"] <= end)]

freq_df = access_frequency(df_range, freq="D")

print(freq_df.head())
