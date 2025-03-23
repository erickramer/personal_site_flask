.PHONY: install-frontend build-frontend dev-frontend clean-frontend run-app

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

# Application Commands
run-app:
	export FLASK_APP=app.py && export FLASK_DEBUG=1 && flask run

# Combined Commands
setup: install-frontend build-frontend

# Default
all: setup