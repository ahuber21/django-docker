# Django Saufhängerle

Here is an excellent guide how to Dockerize Django

https://testdriven.io/blog/dockerizing-django-with-postgres-gunicorn-and-nginx/

## dev + prod environments

The development environment is defined by the files: docker-compose.yml, Dockerfile, .env, etc.
The production envioronment is setup with the corresponding files with .prod in their names.

## Development

Development can be done locally (on the host machine) or in the dev Docker environment.
Some services like the Node-RED to Django communication are only available when running in Docker.


Install Python 3.10 and install the virtual environment with poetry

```bash
pyenv shell 3.10.3
python --version # assert correct version is used
curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python -
poetry shell
poetry install
```

Option 1) Run the server locally

```python
python manage.py migrate
python manage.py collectstatic
python manage.py createsuperuser
python manage.py runserver
```

Option 2) Run the server in the development docker container

```bash
docker compose up -d --build # --build only required after changes
# create a superuser - only required once
docker-compose exec web python manage.py createsuperuser
```

## Production environment

Run the production docker environment

```bash
docker-compose -f docker-compose.prod.yml up -d --build # --build only required after changes
```