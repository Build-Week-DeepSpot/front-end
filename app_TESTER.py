"""Spotify predicted playlist based on user inputs."""
from flask import Flask, request, render_template, json, url_for, redirect
from functions_TESTER import search_song_data


def create_app():
    """Instantiate the Flask database."""
    app = Flask(__name__)

    @app.route("/", methods=['GET', 'POST'])
    def base():
        """Base view. Asks user to input track to get recommendations"""
        if request.method == 'POST':
            # GETS SONG FROM USER
            search_song = request.form['search_song']
            # GETS ID, NAME, ARTIST, URL FOR SEARCH SONG IN DICTIONARY FORM
            input_track = search_song_data(search_song)

            # SENDS THE ABOVE DICTIONARY TO DEEP_RESULTS_TESTER.HTML
            return render_template('deep_results_TESTER.html', input_track=input_track)

        return render_template('deep_landing.html')

    return app


if __name__ == '__main__':
    create_app().run()
