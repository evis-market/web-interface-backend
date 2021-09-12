# Backend for [evis.market](https://evis.market/)

Frontend is built on Vue.js in the [separate repo](https://github.com/evis-market/web-interface-frontend).

## Requirements
* Linux
* Python 3.8+ installed
* make and dev tools (optional)

## Configuration


## Installation

If you have `make` installed - run
```sh
make help
```

### Install by one command:
```sh
./install.sh
```

### Step by step installation

Create virtual environment:
```sh
cd src && python3 -m venv .venv
```

Activate virtual environment:
```sh
source .venv/bin/activate
```

Upgrade pip:
```sh
pip3 install --upgrade pip
```

Install dependencies:
```sh
pip3 install -r ../requirements.dev.txt
```

Create database and load initial data:
```sh
./manage.py migrate
./manage.py createsuperuser
./manage.py loaddata initial.json
```

Run tests:
```bash
$ pytest .
```

Run development server:

```bash
$ ./manage.py runserver

```

**Server will be accessible by http://localhost:8000/**

## Code requirements

### Style

* English only everywhere: docs, comments, commit messages...
* Every class, class method, class propery, model, model field should have a docstring.
* Use [django's style guide](https://docs.djangoproject.com/en/dev/internals/contributing/writing-code/coding-style/#model-style).
* Configure your IDE to use [flake8](https://pypi.python.org/pypi/flake8) for checking your python code. For running flake8 manualy, do `cd src && flake8`
* Commit messages should contain the unique id of issue they are linked to (refs #12345)

### Code organisation

* Prefer simple code (KISS)
* Prefer few small classes over one big.
* **No logic allowed in views or templates**. Only services (separate class) and models.
* Do not use [signals](https://docs.djangoproject.com/en/3.2/topics/signals/).
* Read [django best practices](http://django-best-practices.readthedocs.io/en/latest/index.html)
* Use PEP-484 [type hints](https://www.python.org/dev/peps/pep-0484/) when possible.
* Prefer [Manager](https://docs.djangoproject.com/en/3.2/topics/db/managers/) methods over static methods.
* No l10n is allowed in python code, use [django translation](https://docs.djangoproject.com/en/3.2/topics/i18n/translation/).
