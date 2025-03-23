from flask import Flask, render_template, redirect, jsonify, request
import os
import logging

# Import db from models to avoid circular imports
from models import db

# Import sentiment-related modules
from sentiment.ml import SentimentModel
from sentiment.emojis import emojis

# Initialize sentiment model lazily when needed
_sentiment_model = None

def get_sentiment_model():
    global _sentiment_model
    if _sentiment_model is None:
        _sentiment_model = SentimentModel()
    return _sentiment_model

def create_app(test_config=None):
    # Create Flask application
    app = Flask(__name__)
    
    # Set default configuration
    app.config['BASE_DIR'] = os.getcwd()
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.getcwd() + '/data/tweets.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    # Override with test config if provided
    if test_config:
        app.config.update(test_config)
    
    # Initialize extensions
    db.init_app(app)
    
    # Initialize SQLAlchemy within app context
    with app.app_context():
        # Set text_factory for SQLite connections
        db.engine.raw_connection().text_factory = str
    
    # Register all routes
    register_routes(app)
    
    return app

def register_routes(app):
    """Register all application routes"""
    # Main site routes
    @app.route("/")
    def index():
        return render_template("index.html")
    
    @app.route("/contact")
    def contact():
        return render_template("contact.html")
    
    @app.route("/demos")
    def demos():
        return render_template("demos.html")
    
    @app.route("/about")
    def about():
        return render_template("about.html")
    
    @app.route("/asteroids")
    def asteroids():
        return render_template("asteroids.html")
    
    @app.route("/phone")
    def phone():
        return render_template("phone.html")
    
    @app.route("/email")
    def email():
        return render_template("email.html")
    
    @app.route("/resume")
    def resume():
        return redirect("https://github.com/erickramer/resume/blob/master/EricKramer-resume.pdf")
    
    # Sentiment analysis routes
    @app.route("/sentiment")
    def sentiment_index():
        return render_template("sentiment/sentiment.html")
    
    @app.route("/sentiment/api/score", methods=['POST'])
    def sentiment_score():
        text = request.form['text']
        model = get_sentiment_model()
        res = model.score(text)
        return jsonify(res)

# Create the application instance
app = create_app()
    
if __name__ == "__main__":
    app.run(debug=True)