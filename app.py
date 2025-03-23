from flask import Flask, render_template, redirect
import os

# Import db from models to avoid circular imports
from models import db

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
        
        # Register all blueprints
        register_blueprints(app)
    
    # Register routes for main app
    register_routes(app)
    
    return app

def register_blueprints(app):
    """Register all blueprint modules"""
    # Register the sentiment blueprint
    from sentiment import bp as sentiment_blueprint
    app.register_blueprint(sentiment_blueprint, url_prefix="/sentiment")
    
    # Register image recognition blueprint (currently disabled)
    # from image_recog import bp as image_blueprint
    # app.register_blueprint(image_blueprint, url_prefix="/image")

def register_routes(app):
    """Register routes for the main application"""
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

# Create the application instance
app = create_app()
    
if __name__ == "__main__":
    app.run(debug=True)