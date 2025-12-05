# Personal Site Flask Application

A personal portfolio and demos website built with Flask and Elm-powered interactivity.

## Quick Start

```bash
# Create and activate a virtual environment (optional but recommended)
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install all dependencies and build assets
make setup

# Start the Flask application
make run-app
```

`make setup` detects if a virtual environment is active. When `VIRTUAL_ENV`
is set (e.g. after running `source venv/bin/activate`), dependencies are
installed into that environment. Otherwise packages are installed system wide,
which is useful in the cloud workspace.

Then visit http://localhost:5000 in your browser.

## Testing

The application includes backend and Elm test suites.

### Running All Tests

```bash
# Run all tests (backend and Elm)
make test-all

# Generate coverage reports for all tests
make coverage-all
```

### Backend Testing

To run the backend tests, first install the testing dependencies:

```bash
pip install -e ".[dev]"
```

Then you can run the tests with:

```bash
# Run all backend tests
make test-backend
# or directly with pytest
pytest

# Run tests with coverage report
pytest --cov=./ --cov-report=term

# Generate HTML coverage report
pytest --cov=./ --cov-report=html

# Run specific test categories
pytest -m routes  # Just route tests

# Run tests in verbose mode
pytest -v
```

The backend test suite includes:
- Configuration tests
- Route tests

Tests are automatically run via GitHub Actions when pushing to the master branch or creating a pull request. The application is also automatically deployed to Google App Engine when changes are merged to the master branch.

## Deployment

The application is automatically deployed to Google App Engine when changes are merged to the master branch on GitHub.

### Setting Up Automatic Deployment

To set up automatic deployment, you need to:

1. Create a Google Cloud Project and enable the App Engine API
2. Create a Service Account with App Engine Admin and Storage Admin roles
3. Download the Service Account key as JSON
4. Add the following secrets to your GitHub repository:
   - `GCP_PROJECT_ID`: Your Google Cloud Project ID
   - `GCP_SA_KEY`: The entire content of the downloaded Service Account JSON key file

The GitHub Actions workflow in `.github/workflows/deploy.yml` will handle the rest, automatically deploying your application when changes are merged to the master branch. The workflow invokes the Makefile's `deploy` target so your static assets are built before `gcloud` uploads the app.

### Manual Deployment

If you want to deploy manually using the Google Cloud SDK, make sure the compiled
Elm assets are available. The provided Makefile includes a `deploy` target that
builds the Elm bundles and then runs `gcloud app deploy`:

```bash
make deploy
```

This command ensures that the Elm-generated JavaScript is up to date before uploading the
application to App Engine.

## Project Overview

This Flask-based personal site combines traditional web technologies with modern approaches like Elm and a collection of interactive demos.

### Key Features

- Portfolio pages with contact information
- Interactive Elm-based homepage with particle animations
- Tweet sentiment analyzer with emoji visualization
- Multiple interactive demos including an Asteroids game and visualization experiments
- Terminal-friendly landing page that outputs OSC-8 hyperlinks

## Technologies

- **Backend**: Flask, Python
- **Frontend**: HTML/CSS (Skeleton CSS framework), JavaScript
- **UI Framework**: Elm for interactive components
- **Build System**: Elm CLI via Make targets
- **Libraries**: P5.js, ml5.js, Underscore.js

## Frontend Development

The frontend relies on Elm for the homepage and Asteroids mini-game, with lightweight vanilla JavaScript helpers.

### Elm

```bash
# Build Elm files (requires elm to be installed)
make build-elm

# Run Elm reactor for development (http://localhost:8000)
make dev-elm
```

Note: Elm and `elm-test` must be installed globally for the build and test commands to work. `make setup` will install them automatically if they are missing.

### Elm Testing

```bash
# Run Elm tests
make test-elm
```

The `test-all` target also runs Elm tests alongside the backend suite.

## Project Structure

- **app.py**: Main Flask application and route definitions
- **templates/**: HTML templates for individual pages
- **static/**: Hand-authored CSS/JS plus compiled Elm outputs
- **elm/**: Elm source files for interactive UI components
- **tests/**: Pytest suites covering routes and configuration
- **scripts/** and **Makefile**: Helper commands for development and deployment

## Notable Components

### Elm Integration
- Home page uses Elm for interactive particle animations
- Dynamic resizing based on window dimensions
- Link visualization through particle effects

### Asteroids Mini-Game
- P5.js and Elm-powered gesture-controlled Asteroids experience
- Served as a standalone page with minimal Flask involvement

### Interactive Demos
- `/demos` landing page featuring the Asteroids game, sentiment analyzer, and financial planning visualizer
- Shares Elm animations and assets with the homepage for a consistent feel

### Interactive Demos
- `/demos` landing page featuring the Asteroids game, sentiment analyzer, and financial planning visualizer
- Shares Elm animations and assets with the homepage for a consistent feel

```bash
# Build Elm files (requires elm to be installed)
make build-elm

# Run Elm reactor for development (http://localhost:8000)
make dev-elm
```

Note: Elm and `elm-test` must be installed globally for the build and test commands to work. `make setup` will install them automatically if they are missing.

### Elm Testing

```bash
# Run Elm tests
make test-elm
```

The `test-all` target also runs Elm tests alongside the backend suite.

## Project Structure

- **app.py**: Main Flask application and route definitions
- **templates/**: HTML templates for individual pages
- **static/**: Hand-authored CSS/JS plus compiled Elm outputs
- **elm/**: Elm source files for interactive UI components
- **tests/**: Pytest suites covering routes and configuration
- **scripts/** and **Makefile**: Helper commands for development and deployment

## Notable Components

### Elm Integration
- Home page uses Elm for interactive particle animations
- Dynamic resizing based on window dimensions
- Link visualization through particle effects

### Asteroids Mini-Game
- P5.js and Elm-powered gesture-controlled Asteroids experience
- Served as a standalone page with minimal Flask involvement
