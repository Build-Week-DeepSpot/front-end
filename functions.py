import os
import spotipy
from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from spotipy.oauth2 import SpotifyClientCredentials

DB = SQLAlchemy()
api = spotipy.Spotify()


class Spotify(DB.Model):
    """Set Flask class values for results."""

    id = DB.Column(DB.Integer, primary_key=True, nullable=False)
    genre = DB.Column(DB.String, nullable=False)
    sub_genre = DB.Column(DB.String, nullable=False)
    artist = DB.Column(DB.String, nullable=False)
    album = DB.Column(DB.String, nullable=False)
    title = DB.Column(DB.String, nullable=False)
    tempo = DB.Column(DB.Float, nullable=False)
    length = DB.Column(DB.Integer, nullable=False)

    def __repr__(self):
        return f"[ID: {self.id} | Genre: {self.genre} | Sub-Genre: {self.sub_genre} | Artist: {self.artist} | Album: {self.album} | Title: {self.title} | Tempo: {self.tempo} | Length: {self.length}]"


def get_recommendations(search):
    """Get 10 recommendations from a search."""
    sp = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials())
    # Search: return JSON of the first result
    result = sp.search(q=search, type="track", limit=1)
    # Get ID of the track. Need a list for the recommendation lookup
    id_list = [result["tracks"]["items"][0]["id"]]
    return sp.recommendations(seed_tracks=id_list, limit=10)


def get_covers(recommendations):
    """Get album covers for recommendations."""
    sp = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials())
    id_list = [track["id"] for track in recommendations["tracks"]]
    tracks = sp.tracks(id_list)
    cover_links = [image["album"]["images"][2]["url"] for image in tracks["tracks"]]
    return cover_links


def display(recommendations, covers):
    html_display = ''
    for idx, track in enumerate(recommendations['tracks']):
        html_display += f'''
            <div class = 'row recommendation'>
                <div class = 'col-md-2'>
                    <img src = "{covers[idx]}">
                </div>
                <div class = 'col-md-6 info'>
                    <p>{track['name']} by {track['artists'][0]['name']}</p>
                </div>
                <div class = 'col-md-4'>
                    <a href = "{track['external_urls']['spotify']}" target = '_blank'><button class = 'button'>Play It</button></a>
                </div>
            </div>
        '''
    return html_display


## ** Function added by Carl: Aug 23 ** 

import pandas as pd
from sklearn.neighbors import NearestNeighbors


# Load CSV files
# Embeddings
emb_file = '../../data/embeddings_df_001.csv' # USE CORRECT PATH
embeddings = pd.read_csv(emb_file)
# Drop extra index column
embeddings.drop('Unnamed: 0', axis=1, inplace=True)
# Tracks
track_file = '../../data/tracks.csv'
tracks = pd.read_csv(track_file) # USE CORRECT PATH


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
    # Remove search song if present
    for i in n_indices:
        if i == song_index:
            index = n_indices.index(i)
            n_indices.pop(index)
    # Add search song index at beginning
    n_indices.insert(0, song_index)

    # FIRST INDEX IS SEARCH SONG!
    return n_indices