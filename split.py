import pandas as pd

def dividir_csv(archivo, num_partes=2):
    df = pd.read_csv(archivo)
    tamaño_parte = len(df) // num_partes
    
    for i in range(num_partes):
        inicio = i * tamaño_parte
        fin = None if i == num_partes - 1 else (i + 1) * tamaño_parte
        
        parte = df.iloc[inicio:fin]
        parte.to_csv(f'spotify_stats_part_{i+1}.csv', index=False)
        print(f"Parte {i+1}: {len(parte)} filas")

# Dividir en 3 partes
dividir_csv('data_cache/kagglehub_cache/datasets/datasets/asaniczka/top-spotify-songs-in-73-countries-daily-updated/versions/608/spotify_songs_stats.csv', num_partes=80)