import os
import urllib.parse

from requests import get

LARYNX_HOST = os.environ["LARYNX_HOST"]
LARYNX_VOICE = urllib.parse.quote(os.environ["LARYNX_VOICE"], safe="")
LARYNX_VOCODER = urllib.parse.quote(os.environ["LARYNX_VOCODER"], safe="")
LARYNX_DENOISER_STRENGTH = os.environ["LARYNX_DENOISER_STRENGTH"]
LARYNX_NOISE_SCALE = os.environ["LARYNX_NOISE_SCALE"]
LARYNX_LENGTH_SCALE = os.environ["LARYNX_LENGTH_SCALE"]


def get_wav(text: str) -> bytes:
    url = f"{LARYNX_HOST}/api/tts"
    url += f"?voice={LARYNX_VOICE}"
    url += f"&{text=}"
    url += f"&vocoder={LARYNX_VOCODER}"
    url += f"&denoiserStrength={LARYNX_DENOISER_STRENGTH}"
    url += f"&noiseScale={LARYNX_NOISE_SCALE}"
    url += f"&lengthScale={LARYNX_LENGTH_SCALE}"

    response = get(url)

    if not response or response.status_code != 200:
        raise ValueError(f"Failed to get sound: {response}")

    return response.content
