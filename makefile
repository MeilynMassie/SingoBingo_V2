.PHONY: setup test debug eb
PYTHON := .venv/bin/python
FLASK  := .venv/bin/flask
PIP := .venv/bin/pip
APP_URL := http://127.0.0.1:5000

# Initial setup
setup:
	@echo "STARTING: Creating .venv"
	python3 -m venv .venv
	$(PYTHON) -m pip install --upgrade pip
	@echo "STARTING: Installing dependencies"
	$(PIP) install -r requirements.txt
	@test -f .env || touch .env
	@echo "DONE: Setup .venv and installed dependencies."

# Update requirements.txt with dependencies in .venv
freeze:
	@echo "Starting: Updating requirements.txt"
	$(PIP) freeze > requirements.txt
	@echo "DONE: requirements.txt updated."

# Testing without running Flask
test:
	$(PYTHON) -m app.test.test

# So I don't have to use the GUI anymore to debug
debug:
	@$(PYTHON) -m webbrowser $(APP_URL) &
	FLASK_APP=run.py FLASK_ENV=development FLASK_DEBUG=1 $(FLASK) run

# TODO: AWS EB
eb:
	@echo "Starting: AWS Elastic Beanstalk local run"
# 	eb local run
	@echo "DONE: AWS Elastic Beanstalk local run complete."

# TODO: Code formatter checker
format:
	@echo "Starting: Code format check"
# 	black --check app/
	@echo "DONE: Code format check complete."