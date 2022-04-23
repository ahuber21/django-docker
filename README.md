# Django Saufhängerle

## development

Development happens outside of Docker and is using a PostgreSQL database hosted on the your PC/Mac.
The setup is written of macOS with homebrew.


Install PostgreSQL and create the DB

```bash
brew install postgresql  # tested with 14.2_1
brew services start postgresql
createdb saufhaengerle
```

Install Python 3.10 and install the virtual environment with poetry

```bash
pyenv shell 3.10.3
python --version         # assert correct version is used
curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python -
poetry shell
poetry install
```
