SHELL := /bin/bash

HTTP_PORT := 8000

setup: venv upgrade-pip deps migrate load-initial-data createsuperuser ## Setup whole project for production

setup-dev: venv upgrade-pip deps-dev migrate load-initial-data createsuperuser ## Setup whole project for developer

venv: ## Create virtual environment
	python3 -m venv .venv

upgrade-pip: ## Upgrade pip
	@source .venv/bin/activate && pip3 install --upgrade pip

deps: ## Install production dependencies
	@source .venv/bin/activate && pip3 install -r requirements.txt

deps-dev: deps ## Install developer dependencies
	@source .venv/bin/activate && pip3 install -r requirements.dev.txt

migrations: ## Generate database migrations
	@source .venv/bin/activate && cd src && ./manage.py makemigrations

migrate: ## Apply database migrations
	@source .venv/bin/activate && cd src && ./manage.py migrate

load-initial-data: ## Load initial data
	@source .venv/bin/activate && cd ./src && ./manage.py loaddata initial.json

createsuperuser: ## Create admin user
	@source .venv/bin/activate && cd src && ./manage.py createsuperuser

lint: ## Run flake8 linter
	@source .venv/bin/activate && flake8 src

serve: ## Run server in development mode
	@source .venv/bin/activate && cd src && ./manage.py runserver 0.0.0.0:$(HTTP_PORT)

serve-bg: ## Run server in development mode in background
	@source .venv/bin/activate && cd src && nohup ./manage.py runserver 0.0.0.0:$(HTTP_PORT) > ../serve.log 2>&1 &

shell: ## Run django shell
	@source .venv/bin/activate && cd src && ./manage.py shell

test: ## Run tests
	@source .venv/bin/activate && cd src && pytest .

help: ## This help
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

.DEFAULT_GOAL := help
