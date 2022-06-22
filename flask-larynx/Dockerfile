FROM alpine

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

ENV FLASK_APP=flask-larynx
ENV FLASK_ENV=development
ENV FLASK_PORT=1349

# Install packages via alpine package manager
RUN apk add --no-cache \
    python3 python3-dev \
    gcc musl-dev \
    alsa-utils pulseaudio pulseaudio-alsa alsa-plugins-pulse \
    sdl2-dev sdl2_ttf-dev sdl2_image-dev sdl2_mixer-dev \
    mpg123-dev libjpeg-turbo-dev freetype-dev portmidi-dev && \
    python3 -m ensurepip && \
    rm -r /usr/lib/python*/ensurepip && \
    pip3 install --upgrade pip setuptools && \
    rm -r /root/.cache

RUN mkdir -p /home/app/web
WORKDIR /home/app/web

COPY requirements.txt /home/app/web/

ENV LARYNX_HOST="http://larynx:5002"
ENV LARYNX_VOICE="de-de/thorsten-glow_tts"
ENV LARYNX_VOCODER="hifi_gan/universal_large"
ENV LARYNX_DENOISER_STRENGTH=0.005
ENV LARYNX_NOISE_SCALE=0.333
ENV LARYNX_LENGTH_SCALE=0.85

# Install packages and run app
RUN pip install -r requirements.txt
ENTRYPOINT ["python3"]
CMD ["run.py"]
