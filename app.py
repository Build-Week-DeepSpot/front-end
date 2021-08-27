"""Spotify predicted playlist based on user inputs."""
import os
import pandas as pd
import json
import spotipy
from flask import Flask, request, render_template, json, url_for, redirect
from flask_sqlalchemy import SQLAlchemy
from functions import get_recommendations, get_covers, find_neighbors


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


def create_app():
    """Instantiate the Flask database."""
    app = Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///deep_spot.sqlite3"
    DB.init_app(app)

    @app.route("/", methods=['GET', 'POST'])
    def base():
        """Base view. Asks user to input track to get recommendations"""
        if request.method == 'POST':
            return results(search)

        return render_template('deep_landing.html')


    @app.route('/reset')
    def reset_db():
        """Reset the database"""
        DB.drop_all()
        DB.create_all()
        return render_template('deep_reset.html')

    @app.route('/data', methods=['GET', 'POST'])
    def data():
        """Create a page view with all data from the original dataset"""
        df = pd.read_csv('\\Modelling\\Data\\new_songs_cleaned.csv')
        result = df.to_json(orient="index")
        parsed = json.loads(result)
        return json.dumps(parsed, indent=4)

    @app.route('/results', methods=['GET', 'POST'])
    def prediction_results():
        """Results page view showing predictions"""
        results = find_neighbors(prediction_results)
        return results

    return app


if __name__ == '__main__':
    create_app().run()
