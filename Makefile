check-venv:
ifndef VIRTUAL_ENV
    $(error virtualenv is not activated, please activate it by command: source .venv/bin/activate)
endif

setup: check-venv upgrade-pip deps load-initial-data ## Setup whole project for production: venv, deps, load-initial-data

setup-dev: check-venv upgrade-pip deps-dev load-initial-data load-dev-data ## Setup whole project for developer: venv, deps-dev, load-initial-data, load-dev-data

venv: ## Create virtual environment
	python3 -m venv src/.venv

upgrade-pip: ## Upgrade pip
	pip3 install --upgrade pip

deps: ## Install production dependencies
	pip3 install -r requirements.txt

deps-dev: ## Install developer dependencies
	pip3 install -r requirements.dev.txt

load-initial-data: ## Load initial data
#	cd ./src
#	./manage.py migrate
#	./manage.py createsuperuser
#	./manage.py loaddata

load-dev-data: ## Load extra data for developer
#	cd ./src
#	./manage.py migrate
#	./manage.py createsuperuser
#	./manage.py loaddata

lint: ## Run flake8 linter
	flake8 src

help: ## This help
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

.DEFAULT_GOAL := help
