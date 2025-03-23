# Personal Site Flask Application

A personal portfolio and demos website built with Flask, featuring interactive components and machine learning.

## Quick Start

```bash
# Create and activate a virtual environment (optional but recommended)
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install Python dependencies
pip install -r requirements.txt

# Setup frontend (requires Node.js)
make setup

# Start the Flask application
make run-app
```

Then visit http://localhost:5000 in your browser.

## Testing

The application includes a comprehensive test suite using pytest. To run the tests, first install the testing dependencies:

```bash
pip install -e ".[dev]"
```

Then you can run the tests with:

```bash
# Run all tests
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

The test suite includes:
- Unit tests for models and utility functions
- Integration tests for API endpoints
- Configuration tests
- Route tests

Tests are automatically run via GitHub Actions when pushing to the master branch or creating a pull request.

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

The frontend assets are built using webpack. The source files are located in the `frontend/src` directory and the compiled assets are placed in `static/dist`.

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
- **refactored/**: In-progress refactored application structure

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