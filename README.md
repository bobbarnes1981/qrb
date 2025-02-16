# QRB - Online multiple choice question tests

## TODO

* API for getting and creating questions
* database backend
* Interactive UI
* bearer token authentication for API

## Getting started

Create a virtual environment

```bash
python -m venv .venv
```

Enter the virtual environment

```bash
source .venv/bin/activate
```

Install requirements

```bash
pip install -r requirements.txt
```

Run the api

gunicorn --reload --workers 4 --bind 0.0.0.0:8081 src.api.app:app

Run the delivery front end

gunicorn --reload --workers 4 --bind 0.0.0.0:8080 src.delivery.app:app
