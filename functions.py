import os
import spotipy
from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
import pandas as pd
from sklearn.neighbors import NearestNeighbors
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

# Connect to spotify API
spotify = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials())

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
    # 1. Check if song exists: if yes, use first result
    songs = tracks.index[tracks.name == search_song]
    if len(songs) <1:
        return 'ERROR: Not a valid song name'
    else:
        song_index = songs[0]

    # Put desired data from song into dictionary
    song = tracks.iloc[song_index]
    # Spotify ID for song
    id_code = song['id']
    # Get album cover
    track = spotify.track(id_code)
    album_cover_url = track['album']['images'][2]['url']
    song_data = {
        'id': song_index,
        'name': song['name'],
        'artists': song['artists'][2:-2],
        'url': f'https://open.spotify.com/track/{id_code}',
        'album_cover_url': album_cover_url
    }
    return song_data


def find_neighbors(song):
    '''
    Find the nearest neighbors of a song
    1. Checks for song
    2. Loads and process the embeddings into an array
    3. Trains a nearest neighbors model
    4. Finds the 10 nearest neighbors of the given song
    ARGUMENTS: song in string form
    RETURNS: list of indices
    '''
    # 1. Check if song exists: if yes, use first result
    songs = tracks.index[tracks.name == song]
    if len(songs) <1:
        return 'ERROR: Not a valid song name'
    else:
        song_index = songs[0]

    # 2. Prepare song embeddings data
    # Convert dataframe to numpy array
    encoded_songs = embeddings.to_numpy()

    # 3. Train nearest neighbors model on encodings
    # Number of neighbors
    n = 11
    nn = NearestNeighbors(n_neighbors=n, algorithm='ball_tree')
    nn.fit(encoded_songs)

    # 4. Get neigbors of song
    test_encoding = encoded_songs[song_index].reshape(1,-1)
    _, n_indices = nn.kneighbors(test_encoding)
    # Prepare indices
    n_indices = n_indices.tolist()[0]
    output_tracks = []
    # Remove search song if present
    for i in n_indices:
        if i != song_index:
            # Put data from song into dict
            song = tracks.iloc[i]
            id_code = song['id']
            # Spotify ID for song
            id_code = song['id']
            # Get album cover
            track = spotify.track(id_code)
            album_cover_url = track['album']['images'][2]['url']
            song_data = {
                'id': i,
                'name': song['name'],
                'artists': song['artists'][2:-2],
                'url': f'https://open.spotify.com/track/{id_code}',
                'album_cover_url': album_cover_url
            }
            output_tracks.append(song_data)

    return output_tracks

