from venv import create
from flask import Flask, render_template, request, redirect, url_for

import sys

sys.path.append("../src")

import queue_create_playlist


app = Flask(__name__)

@app.route("/")
def hello_world():
    return render_template("index.html")

@app.route("/", methods=["POST"])
def result():
    mood = request.form.get("emo-options")
    username = request.form.get("username")
    selected_playlist = request.form.get("selected_playlist")
    created_playlist = request.form.get("created_playlist")

    try:
        if created_playlist:
            queue_create_playlist.CreatePlaylist(username, selected_playlist, created_playlist, mood)
        else:
            queue_create_playlist.QueueSong(username, selected_playlist, mood)
    except:
        error_text = "An error occurred. Please try again. (Check your Spotify username, playlist name, and that your Spotify is active if queuing)"
        return render_template("index.html", song_submitted=True,
                                                modal_text=error_text)

    return render_template("index.html", song_submitted=True,
                                            modal_text="Your songs have been added!")


# @app.route("/result", methods=["POST"])
# def result():
#     mood = request.form.get("options")
#     username = request.form.get("username")
#     selected_playlist = request.form.get("selected_playlist")
#     created_playlist = request.form.get("created_playlist")
#     return render_template("index.html", emotion=mood,
#                                           username=username,
#                                           selected_playlist=selected_playlist,
#                                           created_playlist=created_playlist,
#                                           song_submitted=True)
