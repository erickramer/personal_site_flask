.PHONY: build-elm dev-elm test-backend test-elm test-all run-app install-elm install-python-deps recreate-venv setup coverage-all deploy clean

PYTHON_BIN ?= python3

# Elm Tooling
install-elm:
	@which elm >/dev/null || npm install -g elm
	@which elm-test >/dev/null || npm install -g elm-test@0.19.1-revision9

build-elm:
	# Compile Home.elm
	elm make elm/Home.elm --output=static/js/home.js --optimize
	# Compile Asteroids.elm
	elm make elm/Asteroids.elm --output=static/js/asteroids.js --optimize

dev-elm:
	# Start elm reactor for development
	elm reactor

clean:
	rm -rf elm-stuff
	rm -rf venv

test-elm:
	elm-test elm/Tests

# Backend Setup Commands
install-python-deps:
	@if [ -n "$$VIRTUAL_ENV" ]; then \
		pip install --upgrade pip; \
		pip install -r requirements.txt; \
		pip install -e .[dev]; \
	else \
		$(PYTHON_BIN) -m pip install --upgrade pip; \
		$(PYTHON_BIN) -m pip install -r requirements.txt; \
		$(PYTHON_BIN) -m pip install -e .[dev]; \
	fi

recreate-venv:
	rm -rf venv
	$(PYTHON_BIN) -m venv venv
	. venv/bin/activate && \
		pip install --upgrade pip && \
		pip install -r requirements.txt && \
		pip install -e .[dev]

# Backend Test Commands
test-backend:
	python -m pytest

# Combined Test Commands
test-all: test-backend test-elm
	@echo "All tests completed!"

# Application Commands
run-app:
	export FLASK_APP=app.py && export FLASK_DEBUG=1 && flask run

# Combined Commands
setup: install-python-deps install-elm build-elm

# Coverage Commands
coverage-all: 
	python -m pytest --cov=./ --cov-report=term

# Default
all: setup

# Deploy to Google App Engine
deploy: build-elm
	gcloud app deploy app.yaml
