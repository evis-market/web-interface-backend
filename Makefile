check-venv:
ifndef VIRTUAL_ENV
    $(error virtualenv is not activated, please activate it by command: source src/.venv/bin/activate)
endif

setup: check-venv upgrade-pip deps migrate load-initial-data createsuperuser ## Setup whole project for production

setup-dev: check-venv upgrade-pip deps-dev migrate load-initial-data createsuperuser## Setup whole project for developer

venv: ## Create virtual environment
	python3 -m venv src/.venv

upgrade-pip: ## Upgrade pip
	pip3 install --upgrade pip

deps: ## Install production dependencies
	pip3 install -r requirements.txt

deps-dev: deps ## Install developer dependencies
	pip3 install -r requirements.dev.txt

migrations: check-venv ## Generate database migrations
	cd src && ./manage.py makemigrations

migrate: check-venv ## Apply database migrations
	cd src && ./manage.py migrate

load-initial-data: check-venv ## Load initial data
	cd ./src && ./manage.py loaddata app/fixtures/initial/*.json

createsuperuser: check-venv ## Create admin user
	cd src && ./manage.py createsuperuser

lint: ## Run flake8 linter
	flake8 src

serve: ## Run server in developmet mode
	cd src && ./manage.py runserver 0.0.0.0:8000

shell:
	cd src && ./manage.py shell

help: ## This help
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

.DEFAULT_GOAL := help
