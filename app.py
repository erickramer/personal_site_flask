from flask import Flask, render_template, redirect, jsonify, request, url_for, send_from_directory, abort
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
        # Import here to avoid circular imports
        from sentiment.ml import SentimentModel
        try:
            _sentiment_model = SentimentModel()
        except Exception as e:
            logging.warning(f"Error initializing sentiment model: {e}")
            # Use a fallback dummy model in case of errors
            try:
                _sentiment_model = SentimentModel(model="dummy")
            except TypeError:
                # Handle case where the model has been mocked in tests
                # and doesn't accept arguments
                _sentiment_model = SentimentModel()
    return _sentiment_model


def create_app(config_name="default"):
    # Create Flask application
    # Define static folder as the root static folder with a static_url_path of /static
    app = Flask(__name__, static_folder="static", static_url_path="/static")
    
    # Enhance logging
    if config_name == "production":
        # Set up logging
        import logging
        import sys
        from logging.handlers import RotatingFileHandler
        
        # Configure logging
        log_level = os.environ.get('LOG_LEVEL', 'INFO')
        log_formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        
        # Check if we're in App Engine
        in_app_engine = os.environ.get('GAE_ENV', '').startswith('standard')
        
        if in_app_engine:
            # In App Engine, log to stdout which gets captured by Cloud Logging
            log_handler = logging.StreamHandler(sys.stdout)
            app.logger.info("Running in App Engine, logging to stdout")
        else:
            # For local development, use file-based logging
            # Create logs directory if it doesn't exist
            logs_dir = os.path.join(app.instance_path, 'logs')
            try:
                os.makedirs(logs_dir)
            except OSError:
                pass
                
            # Use a file handler for local development
            log_handler = RotatingFileHandler(
                os.path.join(logs_dir, 'app.log'),
                maxBytes=1024 * 1024,
                backupCount=5
            )
        
        # Configure the handler
        log_handler.setFormatter(log_formatter)
        log_handler.setLevel(getattr(logging, log_level))
        app.logger.addHandler(log_handler)
        app.logger.setLevel(getattr(logging, log_level))
        
        # Set stronger static file caching for production
        app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 31536000  # 1 year
        
        # Log static file configuration
        app.logger.info(f"Static folder: {app.static_folder}")
        app.logger.info(f"Static URL path: {app.static_url_path}")
        app.logger.info(f"Cache timeout: {app.config['SEND_FILE_MAX_AGE_DEFAULT']}")

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

    # Serve the favicon for browsers that request /favicon.ico
    @app.route("/favicon.ico")
    def favicon():
        """Serve the favicon from the built assets if available."""
        dist_dir = os.path.join(app.static_folder, "dist", "images")
        fallback_dir = os.path.join(app.static_folder, "images")

        if os.path.exists(os.path.join(dist_dir, "favicon.png")):
            return send_from_directory(dist_dir, "favicon.png", mimetype="image/png")
        elif os.path.exists(os.path.join(fallback_dir, "favicon.png")):
            return send_from_directory(fallback_dir, "favicon.png", mimetype="image/png")

        return abort(404)

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
        
    # Debug route to directly serve static files
    @app.route("/debug/file/<path:filepath>")
    def debug_file(filepath):
        from flask import send_from_directory, abort, make_response
        import mimetypes
        
        # Full path to the static file
        full_path = os.path.join(app.static_folder, filepath)
        
        # Check if file exists
        if not os.path.exists(full_path):
            return abort(404, f"File not found: {full_path}")
        
        # Get MIME type
        mime_type, encoding = mimetypes.guess_type(full_path)
        if not mime_type:
            mime_type = 'application/octet-stream'
            
        # Read file content directly
        try:
            with open(full_path, 'rb') as f:
                content = f.read()
        except Exception as e:
            return abort(500, f"Error reading file: {str(e)}")
            
        # Create response
        response = make_response(content)
        response.headers['Content-Type'] = mime_type
        response.headers['Content-Length'] = str(len(content))
        app.logger.info(f"Serving {filepath} with mime type {mime_type}, size {len(content)}")
        return response
        
    # Debug route to directly serve CSS
    @app.route("/debug/css/<path:filename>")
    def debug_css(filename):
        from flask import send_from_directory, abort, make_response
        
        if not filename.endswith('.css'):
            return abort(400, "Only CSS files are allowed")
            
        # Determine if it's in dist or regular css folder
        if filename.startswith('dist/'):
            css_path = os.path.join(app.static_folder, filename)
        else:
            css_path = os.path.join(app.static_folder, 'dist/css', filename)
            
        # Check if file exists
        if not os.path.exists(css_path):
            return abort(404, f"CSS file not found: {css_path}")
            
        # Read file content and return directly
        with open(css_path, 'r') as f:
            content = f.read()
            
        response = make_response(content)
        response.headers['Content-Type'] = 'text/css'
        return response
    
    # Debug route to check static files
    @app.route("/debug/static")
    def debug_static():
        import os
        import mimetypes
        from flask import current_app, jsonify, send_from_directory, request
        
        static_folder = current_app.static_folder
        static_files = []
        
        for root, dirs, files in os.walk(static_folder):
            for file in files:
                file_path = os.path.join(root, file)
                relpath = os.path.relpath(file_path, static_folder)
                url = url_for('static', filename=relpath)
                
                # Get the size and mime type
                size = os.path.getsize(file_path)
                mime_type, _ = mimetypes.guess_type(file_path)
                
                # Check file permissions
                readable = os.access(file_path, os.R_OK)
                
                static_files.append({
                    "path": relpath,
                    "url": url,
                    "size": size,
                    "mime_type": mime_type,
                    "readable": readable
                })
        
        # Sort files by path for easier reading
        static_files.sort(key=lambda x: x["path"])
        
        # Detailed check for CSS files
        css_files = [f for f in static_files if f["path"].endswith('.css')]
        css_checks = []
        
        for css_file in css_files:
            try:
                # Try to access the file through Flask
                full_path = os.path.join(static_folder, css_file["path"])
                with open(full_path, 'rb') as f:
                    content = f.read(100)  # Read just the beginning
                css_checks.append({
                    "path": css_file["path"],
                    "accessible": True,
                    "size": len(content),
                    "content_preview": content[:20].decode('utf-8', errors='replace')
                })
            except Exception as e:
                css_checks.append({
                    "path": css_file["path"],
                    "accessible": False,
                    "error": str(e)
                })
        
        return jsonify({
            "static_folder": static_folder,
            "files": static_files,
            "css_checks": css_checks,
            "app_url_map": str(app.url_map),
            "request_headers": dict(request.headers)
        })


# Create the application instance based on environment
config_name = os.environ.get("FLASK_CONFIG", "default")
app = create_app(config_name)

if __name__ == "__main__":
    app.run()
