FROM python:3.10.3

WORKDIR /home/app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN groupadd -g 1337 app && useradd -u 1337 -g app -s /bin/sh app

ENV HOME=/home/app
ENV APP_HOME=$HOME/web
RUN mkdir $APP_HOME
RUN mkdir $APP_HOME/staticfiles
WORKDIR $APP_HOME

COPY pyproject.toml \
    poetry.lock \
    $APP_HOME

RUN curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python - && \
    . $HOME/.poetry/env \
    pip install --upgrade pip && \
    poetry config virtualenvs.create false && \
    poetry install

COPY . .

RUN chown -R app:app $APP_HOME

USER app

ENTRYPOINT ["/home/app/web/entrypoint.sh"]