import kagglehub
import os
import pandas as pd
import numpy as np # Importamos numpy para cálculos

# --- Setup y Descarga (sin cambios) ---

# Set custom cache directory
os.environ['KAGGLEHUB_CACHE'] = 'C:/Users/josed/Documents/Code/Python/Spotify/data_cache/kagglehub_cache/datasets'
# Download latest version
path = kagglehub.dataset_download("asaniczka/top-spotify-songs-in-73-countries-daily-updated")
print("Path to dataset files:", path)


# Load the datasets into a DataFrame (sin cambios)
df = pd.read_csv(os.path.join(path, 'universal_top_spotify_songs.csv'))

# Enumeración de 'spotify_id' y limpieza (sin cambios)
unique_songs = df['spotify_id'].nunique()
print("Total unique songs:", unique_songs)

spotify_id_to_number = {spotify_id: idx + 1 
                        for idx, spotify_id in enumerate(df['spotify_id'].unique())}
df['spotify_id'] = df['spotify_id'].map(spotify_id_to_number)

df = df[df['popularity'] != 0].reset_index(drop=True)
df['country'] = df['country'].fillna('GLB')

# --- Creación de df_Info (sin cambios) ---

df_Info = df[['spotify_id', 'name', 'artists', 'album_name', 'album_release_date', 'is_explicit', 
              'duration_ms', 'danceability', 'energy', 'key', 'loudness', 'mode', 
              'speechiness', 'acousticness', 'instrumentalness', 'liveness', 
              'valence', 'tempo', 'time_signature']].drop_duplicates(subset=['spotify_id']).reset_index(drop=True)

print(df_Info.head())

# --- Creación de df_Stats ORIGINAL ---

# DataFrame con todas las estadísticas (antes de la reducción)
df_Stats = df[['spotify_id', 'snapshot_date', 'daily_rank', 'daily_movement', 'weekly_movement', 'country', 'popularity']]

# -----------------------------------------------------
## 📉 Reducción Equitativa de df_Stats
# -----------------------------------------------------

# Define el porcentaje de estadísticas a MANTENER (por ejemplo, 0.5 para 50%)
reduction_percentage = 0.41

# Usamos la función 'groupby()' y 'sample()' para reducir equitativamente
# El parámetro 'frac' define la fracción de filas a seleccionar por cada grupo ('spotify_id')
df_Stats_reduced = df_Stats.groupby('spotify_id', group_keys=False).apply(
    lambda x: x.sample(frac=reduction_percentage)
).reset_index(drop=True) # Reseteamos el índice para limpiar

print(f"\nNúmero total de filas de estadísticas antes de la reducción: {len(df_Stats)}")
print(f"Número total de filas de estadísticas después de MANTENER el {reduction_percentage*100}%: {len(df_Stats_reduced)}")
print(df_Stats_reduced.head())

# --- Guardar DataFrames Reducidos (usando df_Stats_reduced) ---

# print total unique songs after cleaning (sin cambios)
unique_songs_info = df_Info['spotify_id'].nunique()
unique_songs_stats = df_Stats_reduced['spotify_id'].nunique()
print("Total unique songs after cleaning (Info):", unique_songs_info)
print("Total unique songs after cleaning (Stats):", unique_songs_stats)


# Guardamos df_Info (sin cambios)
df_Info.to_csv(os.path.join(path, 'spotify_songs_info.csv'), index=False)

# Guardamos df_Stats REDUCIDO
df_Stats_reduced.to_csv(os.path.join(path, 'spotify_songs_stats.csv'), index=False)

print("\nArchivos guardados:")
print("- spotify_songs_info.csv (sin reducción)")
print("- spotify_songs_stats.csv (con reducción equitativa al 50%)")

#count characters in each file and print the total
total_characters = 0
for file_name in ['spotify_songs_info.csv', 'spotify_songs_stats.csv']:
    file_path = os.path.join(path, file_name)
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
        num_characters = len(content)
        total_characters += num_characters
        print(f"{file_name}: {num_characters} characters")
print("Total characters in both files:", total_characters)


# search for a specific song by its original spotify_id
# print("\nSearching by numeric ID:")
# song_number = 2
# song_data = df[df['spotify_id'] == song_number]
# print(f"Data for song ID {song_number}:")
# print(song_data.head(150))

# 

