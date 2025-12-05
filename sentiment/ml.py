import importlib
from flask import current_app

# Import db from models module to avoid circular imports
from models import db
from .emojis import emojis
from .models import Tweet

import os
import logging

_TF_MODULE = None
_TF_LAYERS = {}
TF_IMPORT_ERROR = None

_NP_MODULE = None
NP_IMPORT_ERROR = None


def _ensure_tensorflow():
    """Import TensorFlow lazily to avoid heavy startup costs in tests."""
    global _TF_MODULE, _TF_LAYERS, TF_IMPORT_ERROR
    if _TF_MODULE is not None:
        return
    try:
        tf = importlib.import_module("tensorflow")
        keras_models = importlib.import_module("tensorflow.keras.models")
        keras_layers = importlib.import_module("tensorflow.keras.layers")
    except Exception as exc:
        TF_IMPORT_ERROR = exc
        raise

    _TF_MODULE = tf
    _TF_LAYERS = {
        "Model": keras_models.Model,
        "Input": keras_layers.Input,
        "Dense": keras_layers.Dense,
        "Dropout": keras_layers.Dropout,
        "Embedding": keras_layers.Embedding,
        "LSTM": keras_layers.LSTM,
    }


def _ensure_numpy():
    """Import numpy lazily so tests without the dependency can still run."""
    global _NP_MODULE, NP_IMPORT_ERROR
    if _NP_MODULE is not None:
        return _NP_MODULE
    try:
        np = importlib.import_module("numpy")
    except Exception as exc:
        NP_IMPORT_ERROR = exc
        raise
    _NP_MODULE = np
    return np

def data_gen(batch_size=100):
    np = _ensure_numpy()
    # loading all tweets into memory for speed
    tweets = db.session.query(Tweet).all()

    xs = []
    ys = []
    ss = []

    while True:
        import random
        random.shuffle(tweets)

        for tweet in tweets:
            xs.append(tweet.x)
            ys.append(tweet.y)
            ss.append(tweet.sentiment)

            if len(xs) == batch_size:
                yield np.stack(xs), [np.stack(ys), np.stack(ss)]
                xs = []
                ys = []
                ss = []

class SentimentModel(object):

    def __init__(self, model=None):
        self._is_dummy = False
        self.baseline = [1.0 for _ in emojis]
        if model == "dummy":
            self._use_dummy_model()
        elif model is None:
            try:
                # Check if we're in App Engine production environment
                if os.environ.get('GAE_ENV', '').startswith('standard'):
                    logging.info("Running in App Engine environment, using dummy model")
                    self._use_dummy_model()
                elif os.path.exists(self.model_path):
                    logging.info(f"Loading model from {self.model_path}")
                    self._model = self._load_model()
                else:
                    logging.info("Building new model")
                    self._model = self._build_model()
            except Exception as e:
                logging.warning(f"Failed to load or build model: {e}")
                self._use_dummy_model()
        else:
            self._model = model

        if getattr(self._model, "is_dummy", False):
            self._is_dummy = True

        if not self._is_dummy:
            try:
                self.baseline = self._set_baseline()
            except Exception as e:
                logging.warning(f"Failed to set baseline: {e}")
                self._use_dummy_model()

    @property
    def model_path(self):
        # Use BASE_DIR from config with consistent path handling
        return os.path.join(current_app.config['BASE_DIR'], 'data', 'model.h5')

    def _build_model(self):
        """Build a real LSTM model for sentiment analysis."""
        try:
            _ensure_tensorflow()
        except Exception as exc:
            raise RuntimeError(f"TensorFlow is required to build the model: {exc}") from exc

        text = _TF_LAYERS["Input"](shape=(140,))

        x = _TF_LAYERS["Embedding"](input_dim=5000, output_dim=64)(text)
        x = _TF_LAYERS["LSTM"](128)(x)
        x = _TF_LAYERS["Dropout"](0.5)(x)

        emoji = _TF_LAYERS["Dense"](len(emojis), activation="sigmoid", name="emoji")(x)
        sentiment = _TF_LAYERS["Dense"](3, activation="sigmoid", name="sentiment")(x)

        model = _TF_LAYERS["Model"](text, [emoji, sentiment])

        model.compile("RMSprop",
                  loss={'sentiment': "binary_crossentropy", "emoji": "binary_crossentropy"},
                  loss_weights={"sentiment":0.5, "emoji": 0.5})

        return model
        
    def _build_dummy_model(self):
        """Build a simple dummy model for testing and CI environments."""
        class DummyModel:
            is_dummy = True

            def predict(self, x):
                """Return dummy predictions for testing."""
                emoji_scores = [[0.5 for _ in emojis]]
                sentiment = [[0.7]]
                return emoji_scores, sentiment
                
            def save(self, path):
                """Dummy save method."""
                pass
                
        return DummyModel()

    def _use_dummy_model(self):
        self._model = self._build_dummy_model()
        self._is_dummy = True
        self.baseline = [1.0 for _ in emojis]

    def _load_model(self):
        try:
            _ensure_tensorflow()
        except Exception as exc:
            raise RuntimeError(f"TensorFlow is required to load the model: {exc}") from exc
        return _TF_MODULE.keras.models.load_model(self.model_path)

    def _set_baseline(self):
        tweet = Tweet("")
        x_input = self._prepare_input(tweet.x)
        scores, _ = self._model.predict(x_input)
        return self._flatten_scores(scores)

    def fit(self, batch_size=100, steps_per_epoch=1e3,
            nb_epoch=10, save=True):

        gen = data_gen(batch_size)

        self._model.fit(gen,
                steps_per_epoch=steps_per_epoch,
                epochs=nb_epoch)

        if save:
            self._model.save(self.model_path)

    def score(self, text, normalize = True):
        logging.info("Scoring tweet: %s ", text)

        tweet = Tweet(text)
        x_input = self._prepare_input(tweet.x)

        try:
            scores, sentiment = self._model.predict(x_input)
            emoji_scores = self._flatten_scores(scores)
            sentiment_value = self._flatten_sentiment(sentiment)

            if normalize and not self._is_dummy:
                emoji_scores = self._normalize_scores(emoji_scores)
        except Exception as e:
            logging.error("Failed on tweet: %s. Error: %s", text, str(e))
            emoji_scores = list(self.baseline)
            sentiment_value = 0.0

        scores_dict = dict(zip(emojis, emoji_scores))
        return {"emoji": scores_dict, "sentiment": sentiment_value}

    def _prepare_input(self, vector):
        values = list(vector)
        if self._is_dummy:
            return [values]
        np = _ensure_numpy()
        arr = np.array(values).reshape(1, -1)
        return arr

    def _flatten_scores(self, scores):
        if hasattr(scores, "tolist"):
            scores = scores.tolist()
        if isinstance(scores, (list, tuple)) and scores and isinstance(scores[0], (list, tuple)):
            scores = scores[0]
        return [float(s) for s in scores]

    def _flatten_sentiment(self, sentiment):
        if hasattr(sentiment, "tolist"):
            sentiment = sentiment.tolist()
        if isinstance(sentiment, (list, tuple)):
            if sentiment and isinstance(sentiment[0], (list, tuple)):
                sentiment = sentiment[0]
            if sentiment:
                return float(sentiment[0])
        return float(sentiment)

    def _normalize_scores(self, emoji_scores):
        normalized = []
        for idx, score in enumerate(emoji_scores):
            base = self.baseline[idx] if idx < len(self.baseline) else 1.0
            if base:
                normalized.append(score / base)
            else:
                normalized.append(score)
        return normalized
