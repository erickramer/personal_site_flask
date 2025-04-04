from flask import Flask, render_template, redirect, jsonify, request, url_for
import os
import logging

# Import db from models to avoid circular imports
from models import db

# Import configuration
from config import config

# Import sentiment-related modules
from sentiment.ml import SentimentModel
from sentiment.emojis import emojis

# Initialize sentiment model lazily when needed
_sentiment_model = None


def get_sentiment_model():
    global _sentiment_model
    if _sentiment_model is None:
        try:
            _sentiment_model = SentimentModel()
        except Exception as e:
            logging.warning(f"Error initializing sentiment model: {e}")
            # Use a fallback dummy model in case of errors
            from sentiment.ml import SentimentModel
            _sentiment_model = SentimentModel(model="dummy")
    return _sentiment_model


def create_app(config_name="default"):
    # Create Flask application
    # Define static folder as the root static folder with a static_url_path of /static
    app = Flask(__name__, static_folder="static", static_url_path="/static")

    # Load the appropriate configuration
    app.config.from_object(config[config_name])

    # Ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # Initialize extensions
    db.init_app(app)

    # Initialize SQLAlchemy within app context
    with app.app_context():
        # Only attempt to configure SQLite connection if not in production
        if config_name != "production":
            try:
                # Set text_factory for SQLite connections
                db.engine.raw_connection().text_factory = str
            except Exception as e:
                app.logger.warning(f"Could not set SQLite text_factory: {e}")

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
        user_agent = request.headers.get("User-Agent", "").lower()
        if "curl" in user_agent:
            # Plain text version for curl requests
            return """

I'm Eric Kramer. I currently work at OpenAI helping build the developer platform. 
I used to work at Stripe and Dataiku. A long time ago, I was an MD/PhD student at 
UC San Diego.


I live in Noe Valley, San Francisco with my wife, our two cats and two sons.
Get in touch if you want to talk more about data science or medicine. You 
can reach me at 619.724.3800 or ericransomkramer@gmail.com.

"""
        else:
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
        return redirect(
            "https://github.com/erickramer/resume/blob/master/EricKramer-resume.pdf"
        )

    # Sentiment analysis routes
    @app.route("/sentiment")
    def sentiment_index():
        return render_template("sentiment.html")

    @app.route("/sentiment/api/score", methods=["POST"])
    def sentiment_score():
        text = request.form["text"]
        model = get_sentiment_model()
        res = model.score(text)
        return jsonify(res)


# Create the application instance based on environment
config_name = os.environ.get("FLASK_CONFIG", "default")
app = create_app(config_name)

if __name__ == "__main__":
    app.run()
