import os
import pandas as pd


#search for a specific song by its original spotify_id
path = 'data_cache/kagglehub_cache/datasets/datasets/asaniczka/top-spotify-songs-in-73-countries-daily-updated/versions/608'
df = pd.read_csv(os.path.join(path, 'spotify_songs_info.csv'))
print("\nSearching by numeric ID:")
song_number = 2
song_data = df[df['spotify_id'] == song_number]
print(f"Data for song ID {song_number}:")
print(song_data.head(150))