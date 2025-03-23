# Personal Site Flask Application

A personal portfolio and demos website built with Flask, featuring interactive components and machine learning.

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
- **Data Visualization**: D3.js
- **Machine Learning**: Keras/TensorFlow for sentiment analysis
- **Libraries**: jQuery, Underscore.js
- **Database**: SQLite

## Project Structure

- **app.py**: Main Flask application
- **templates/**: HTML templates for different pages
- **static/**: CSS, JS, images and other static assets
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