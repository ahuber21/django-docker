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
    app.logger.info(f"Requested sentence: {sentence}")
    try:
        wav = get_wav(sentence)
    except ValueError as err:
        app.logger.error(f"Sound generation failed: {err}")
        return "Sound generation failed: {err}"

    app.logger.info(f"Got wav!")
    play(wav)
    return f"Ok: {sentence}"
