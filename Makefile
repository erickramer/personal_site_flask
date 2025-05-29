.PHONY: install-frontend build-frontend build-elm dev-frontend dev-elm clean-frontend test-frontend test-frontend-watch test-frontend-coverage test-backend test-all run-app install-elm install-python-deps

# Frontend Build Commands
install-elm:
	@which elm >/dev/null || npm install -g elm
	@which elm-test >/dev/null || npm install -g elm-test

install-frontend: install-elm
	cd frontend && npm install

build-frontend:
	cd frontend && npm run build
	# Copy the dist directory to static folder
	rm -rf static/dist
	cp -r frontend/dist static/

# Elm Build Commands
build-elm:
	# Compile Home.elm
	elm make elm/Home.elm --output=static/js/home.js --optimize
	# Compile About.elm
	elm make elm/About.elm --output=static/js/about.js --optimize
	# Compile Asteroids.elm
	elm make elm/Asteroids.elm --output=static/js/asteroids.js --optimize

dev-frontend:
	cd frontend && npm run dev

dev-elm:
	# Start elm reactor for development
	elm reactor

clean-frontend:
	rm -rf frontend/node_modules
	rm -rf frontend/dist
	rm -rf static/dist
	rm -rf frontend/coverage
	rm -rf elm-stuff

# Frontend Test Commands
test-frontend:
	cd frontend && npm test

test-frontend-watch:
	cd frontend && npm run test:watch

test-frontend-coverage:
	cd frontend && npm run test:coverage

# Backend Setup Commands
install-python-deps:
	@which uv >/dev/null || pip install uv
	uv pip install --system -r requirements.txt 
	uv pip install --system -e .[dev]

# Backend Test Commands
test-backend:
	python -m pytest

# Combined Test Commands
test-all: test-backend test-frontend
	@echo "All tests completed!"

# Application Commands
run-app:
	export FLASK_APP=app.py && export FLASK_DEBUG=1 && flask run

# Combined Commands
setup: install-python-deps install-frontend build-frontend build-elm

# Coverage Commands
coverage-all: 
	python -m pytest --cov=./ --cov-report=term
	cd frontend && npm run test:coverage

# Default
all: setup

# Deploy to Google App Engine
deploy: build-frontend build-elm
	gcloud app deploy app.yaml
