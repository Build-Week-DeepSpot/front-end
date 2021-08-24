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