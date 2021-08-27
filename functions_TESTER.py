import pandas as pd

# Load CSV files

# Embeddings
emb_file = 'Modelling/Data/autoencoder_embeddings.csv'
# emb_file = 'C:/Users/mattr/Repositories/Unit3BuildWeek/Modelling/Data/autoencoder_embeddings.csv' # USE CORRECT PATH
embeddings = pd.read_csv(emb_file)
# Drop extra index column
embeddings.drop('Unnamed: 0', axis=1, inplace=True)

# Tracks
track_file = 'Modelling/Data/tracks_drop_duplicates.csv'
# track_file = 'C:/Users/mattr/Repositories/Unit3BuildWeek/Modelling/Data/tracks_drop_duplicates.csv'
tracks = pd.read_csv(track_file) # USE CORRECT PATH


def search_song_data(search_song):
    # Check if song exists: if yes, use first result
    songs = tracks.index[tracks.name == search_song]
    if len(songs) < 1:
        return 'ERROR: Not a valid song name'
    else:
        song_index = songs[0]

    # Put desired data from song into dictionary
    song = tracks.iloc[song_index]
    id_code = song['id']
    song_data = {
        'id': song_index,
        'name': song['name'],
        'artists': song['artists'][2:-2],
        'url': f'https://open.spotify.com/track/{id_code}'
    }
    return song_data
