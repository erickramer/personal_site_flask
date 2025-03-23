.PHONY: install-frontend build-frontend dev-frontend clean-frontend test-frontend test-frontend-watch test-frontend-coverage test-backend test-all run-app

# Frontend Build Commands
install-frontend:
	cd frontend && npm install

build-frontend:
	cd frontend && npm run build
	# Copy the dist directory to static folder
	rm -rf static/dist
	cp -r frontend/dist static/

dev-frontend:
	cd frontend && npm run dev

clean-frontend:
	rm -rf frontend/node_modules
	rm -rf frontend/dist
	rm -rf static/dist
	rm -rf frontend/coverage

# Frontend Test Commands
test-frontend:
	cd frontend && npm test

test-frontend-watch:
	cd frontend && npm run test:watch

test-frontend-coverage:
	cd frontend && npm run test:coverage

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
setup: install-frontend build-frontend

# Coverage Commands
coverage-all: 
	python -m pytest --cov=./ --cov-report=term
	cd frontend && npm run test:coverage

# Default
all: setup