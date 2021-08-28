"""Spotify predicted playlist based on user inputs."""
import spotipy
from flask import Flask, request, render_template
from functions import find_neighbors, search_song_data


api = spotipy.Spotify()


def create_app():
    """Instantiate the Flask database."""
    app = Flask(__name__)


    @app.route("/", methods=['GET', 'POST'])
    def base():
        """Base view. Asks user to input track to get recommendations"""
        if request.method == 'POST':
            # Get songs from user
            search_song = request.form['search_song']
            # Get ID, name, artist, url for search_song in dict form
            input_track = search_song_data(search_song)
            # Get recommended songs
            output_tracks = find_neighbors(search_song)
            # Sends the above dict to deep_results.html
            return render_template('deep_results.html', input_track=input_track, output_tracks=output_tracks)


        return render_template('deep_landing.html')

    return app


if __name__ == '__main__':
    create_app().run(port=1000)
