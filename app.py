from flask import Flask, render_template, redirect
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)

app.config['BASE_DIR'] = os.getcwd()
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.getcwd() + '/data/tweets.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
db.engine.raw_connection().text_factory = str

from sentiment import app as sentiment_blueprint
app.register_blueprint(sentiment_blueprint, url_prefix="/sentiment")

# from image_recog import app as image_blueprint
# app.register_blueprint(image_blueprint, url_prefix="/image")

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