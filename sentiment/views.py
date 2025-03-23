from flask import render_template, jsonify, request, current_app
from sentiment import bp
from sentiment.ml import SentimentModel

# Initialize sentiment model lazily when needed
_sentiment_model = None

def get_sentiment_model():
    global _sentiment_model
    if _sentiment_model is None:
        _sentiment_model = SentimentModel()
    return _sentiment_model

@bp.route('/')
def index():
    return render_template('sentiment.html')

@bp.route('/api/score', methods=['POST'])
def score():
    text = request.form['text']
    model = get_sentiment_model()
    res = model.score(text)
    return jsonify(res)

@bp.route('/static/<path:path>')
def static_file(path):
    return bp.send_static_file(path)
