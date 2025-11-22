import kagglehub
import os
import pandas as pd

# Set custom cache directory
os.environ['KAGGLEHUB_CACHE'] = 'C:/Users/josed/Documents/Code/Python/Spotify/data_cache/kagglehub_cache/datasets'
# Download latest version
path = kagglehub.dataset_download("asaniczka/top-spotify-songs-in-73-countries-daily-updated")
print("Path to dataset files:", path)


# Todo: reduce total character usage

# Load the datasets into a DataFrame
df = pd.read_csv(os.path.join(path, 'universal_top_spotify_songs.csv'))

# we find each unique song by its 'track_id'
unique_songs = df['spotify_id'].nunique()
print("Total unique songs:", unique_songs)

# replace 'spotify_id' with  enumeration from 1 to n unique_songs   
spotify_id_to_number = {spotify_id: idx + 1 
                        for idx, spotify_id in enumerate(df['spotify_id'].unique())}

df['spotify_id'] = df['spotify_id'].map(spotify_id_to_number)

# delete all instances of rows where 'popularity' is 0 
df = df[df['popularity'] != 0].reset_index(drop=True)

# replace all NaN values in country column with 'GLB'
df['country'] = df['country'].fillna('GLB')

# Create a copy of the df with the following columns only: spotify_id, name, artists, album_name, album_release_date, is_explicit, 
# duration_ms, danceability, energy, key, loudness, mode, speechiness, acousticness, instrumentalness, liveness, valence, tempo, time_signature
# using only the first occurrence of each spotify_id (i.e., drop duplicates)
df_Info = df[['spotify_id', 'name', 'artists', 'album_name', 'album_release_date', 'is_explicit', 
         'duration_ms', 'danceability', 'energy', 'key', 'loudness', 'mode', 
         'speechiness', 'acousticness', 'instrumentalness', 'liveness', 
         'valence', 'tempo', 'time_signature']].drop_duplicates(subset=['spotify_id']).reset_index(drop=True)

print(df_Info.head())

# create another DataFrame with the following columns only: spotify_id, snapshot_date, daily_rank, daily_movement, weekly_movement, country, popularity
# using all occurrences of each spotify_id
df_Stats = df[['spotify_id', 'snapshot_date', 'daily_rank', 'daily_movement', 'weekly_movement', 'country', 'popularity']]
print(df_Stats.head())

# print total unique songs after cleaning
unique_songs = df_Info['spotify_id'].nunique()
print("Total unique songs after cleaning:", unique_songs)


# save both DataFrames to csv files
df_Info.to_csv(os.path.join(path, 'spotify_songs_info.csv'), index=False)
df_Stats.to_csv(os.path.join(path, 'spotify_songs_stats.csv'), index=False)


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

