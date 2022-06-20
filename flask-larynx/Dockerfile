FROM alpine

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

ENV FLASK_APP=flask-larynx
ENV FLASK_ENV=development
ENV FLASK_PORT=1349

# Install packages via alpine package manager
RUN apk add --no-cache python3 && \
    python3 -m ensurepip && \
    rm -r /usr/lib/python*/ensurepip && \
    pip3 install --upgrade pip setuptools && \
    rm -r /root/.cache

RUN mkdir -p /home/app/web
WORKDIR /home/app/web

COPY requirements.txt /home/app/web/

# Install packages and run app
RUN pip install -r requirements.txt
ENTRYPOINT ["python3"]
CMD ["run.py"]
