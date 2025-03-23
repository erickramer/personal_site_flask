from sentiment import app
from flask import render_template, jsonify, request
from sentiment.ml import SentimentModel

sentiment_model = SentimentModel()

@app.route('/')
def index():
    print("hello, eric")
    return render_template('sentiment.html')

@app.route('/api/score', methods=['POST'])
def score():
    text = request.form['text']
    res = sentiment_model.score(text)
    return jsonify(res)

@app.route('/static/<path:path>')
def static_file(path):
    return app.send_static_file(path)
