from adaptadores.load import load_events

path = "datos/exports/logs_KX7A_20260220-1944_GrupoB.json"

df = load_events(path)

print(df.head())
print(df.columns)
print(len(df))