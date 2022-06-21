from app import app
from app.larynx import get_wav
from app.player import play
from flask import request


@app.route("/")
@app.route("/index")
def index():
    return "Hello, World!"


@app.route("/talk/<string:sentence>", methods=["GET"])
def talk(sentence):
    try:
        wav = get_wav("test")
    except ValueError as err:
        return "Sound generation failed: {err}"

    play(wav)
    return ""
