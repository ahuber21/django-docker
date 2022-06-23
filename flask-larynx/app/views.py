from time import time

from app import app
from app.larynx import get_wav
from app.player import play


@app.route("/")
@app.route("/index")
def index():
    return "Hello, World!"


@app.route("/talk/<string:sentence>", methods=["GET"])
def talk(sentence: str):
    app.logger.info(f"Requested sentence: {sentence}")
    start = time()
    try:
        wav = get_wav(sentence)
    except ValueError as err:
        app.logger.error(f"Sound generation failed: {err}")
        return f"Sound generation failed: {err}"

    app.logger.info(f"Got wav! Took {1000. * (time() - start):.0f} ms")
    play(wav)
    return f"Ok: {sentence} [{1000. * (time() - start):.0f} ms]"
