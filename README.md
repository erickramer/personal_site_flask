# Personal Site Flask Application

A personal portfolio and demos website built with Flask, featuring interactive components and machine learning.

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

The application includes comprehensive test suites for both backend and frontend code.

### Running All Tests

```bash
# Run all tests (both backend and frontend)
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
pytest -m sentiment  # Just sentiment module tests

# Run tests in verbose mode
pytest -v
```

The backend test suite includes:
- Unit tests for models and utility functions
- Integration tests for API endpoints
- Configuration tests
- Route tests

### Frontend Testing

```bash
# Run all frontend tests
make test-frontend

# Run frontend tests in watch mode (for development)
make test-frontend-watch

# Generate frontend test coverage report
make test-frontend-coverage
```

The frontend test suite includes:
- Component tests using Jest and Testing Library
- Unit tests for utility functions
- Integration tests for API interactions
- Mock tests for third-party libraries (D3, etc.)

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
static assets are available. The provided Makefile includes a `deploy` target that
builds the frontend and Elm assets and then runs `gcloud app deploy`:

```bash
make deploy
```

This command ensures that `static/dist` is populated before uploading the
application to App Engine.

## Project Overview

This Flask-based personal site combines traditional web technologies with modern approaches like Elm and machine learning.

### Key Features

- Portfolio pages with contact information
- Interactive Elm-based homepage with particle animations
- Sentiment analysis module for analyzing tweet sentiment
- Multiple interactive demos including an Asteroids game
- Data visualization using D3.js

## Technologies

- **Backend**: Flask, SQLAlchemy, Python
- **Frontend**: HTML/CSS (Skeleton CSS framework), JavaScript
- **UI Framework**: Elm for interactive components
- **Build System**: Webpack, Babel, SASS
- **Data Visualization**: D3.js
- **Machine Learning**: Keras/TensorFlow for sentiment analysis
- **Libraries**: jQuery, Underscore.js
- **Database**: SQLite

## Frontend Development

The frontend uses a combination of JavaScript (built with webpack) and Elm:

### JavaScript/CSS

The JavaScript/CSS assets are built using webpack. The source files are located in the `frontend/src` directory and the compiled assets are placed in `static/dist`.

```bash
# Install frontend dependencies
make install-frontend

# Build frontend assets for production
make build-frontend

# Watch for changes during development
make dev-frontend

# Clean frontend build artifacts
make clean-frontend
```

### Elm

The application also uses Elm for interactive components:

```bash
# Build Elm files (requires elm to be installed)
make build-elm

# Run Elm reactor for development (http://localhost:8000)
make dev-elm
```

Note: Elm and `elm-test` must be installed globally for the build and test commands to work. `make setup` will install them automatically if they are missing.

### Frontend Testing

The frontend includes a comprehensive Jest test suite:

```bash
# Run all frontend tests
make test-frontend

# Run frontend tests in watch mode (for development)
make test-frontend-watch

# Generate frontend test coverage report
make test-frontend-coverage
```

The test suite includes:
- Component tests using Jest and Testing Library
- Unit tests for utility functions
- Integration tests for API interactions
- Mock tests for third-party libraries (D3, etc.)

## Project Structure

- **app.py**: Main Flask application
- **templates/**: HTML templates for different pages
- **static/**: CSS, JS, images and other static assets
  - **dist/**: Compiled and minified frontend assets
- **frontend/**: Frontend source files
  - **src/**: Source JavaScript and CSS
  - **webpack.config.js**: Webpack configuration
- **sentiment/**: Sentiment analysis module
  - Machine learning model (ml.py)
  - Tweet models (models.py)
  - Emoji handling (emojis.py)
  - Views and routes (views.py)
- **elm/**: Elm source files for interactive UI components
- **data/**: Database files and ML model storage

## Notable Components

### Sentiment Analysis Module
- Uses Keras LSTM neural network for sentiment prediction
- Analyzes text for emoji predictions
- Interactive visualization of sentiment scores
- Trained on tweet data stored in SQLite database

### Elm Integration
- Home page uses Elm for interactive particle animations
- Dynamic resizing based on window dimensions
- Link visualization through particle effects

### Interactive Demos
- Asteroids game implementation
- Multiple visualization demos