from flask import current_app

# Import db from models module to avoid circular imports
from models import db
from .emojis import emojis
from .models import Tweet

import os
import numpy as np
import logging
import importlib

def data_gen(batch_size=100):
    # loading all tweets into memory for speed
    tweets = db.session.query(Tweet).all()

    xs = []
    ys = []
    ss = []

    while True:
        np.random.shuffle(tweets)

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
        self._tf = None
        if model == "dummy":
            # Explicitly use dummy model
            self._model = self._build_dummy_model()
            logging.info("Using dummy sentiment model")
        elif model is None:
            try:
                # Check if we're in App Engine production environment
                if os.environ.get('GAE_ENV', '').startswith('standard'):
                    logging.info("Running in App Engine environment, using dummy model")
                    self._model = self._build_dummy_model()
                elif os.path.exists(self.model_path):
                    logging.info(f"Loading model from {self.model_path}")
                    self._model = self._load_model()
                else:
                    logging.info("Building new model")
                    self._model = self._build_model()
            except Exception as e:
                # For testing and CI environments, create a dummy model
                logging.warning(f"Failed to load or build model: {e}")
                self._model = self._build_dummy_model()
        else:
            self._model = model

        try:
            self._set_baseline()
        except Exception as e:
            logging.warning(f"Failed to set baseline: {e}")
            # Set a default baseline for testing
            import numpy as np
            self.baseline = np.ones((1, len(emojis)))

    @property
    def model_path(self):
        # Use BASE_DIR from config with consistent path handling
        return os.path.join(current_app.config['BASE_DIR'], 'data', 'model.h5')

    def _get_tf(self):
        """Import TensorFlow lazily so environments without it can still run."""
        if self._tf is not None:
            return self._tf

        try:
            tf = importlib.import_module("tensorflow")
        except Exception as exc:
            raise RuntimeError("TensorFlow is not available") from exc

        self._tf = tf
        return tf

    def _build_model(self):
        """Build a real LSTM model for sentiment analysis."""
        tf = self._get_tf()

        text = tf.keras.Input(shape=(140,))

        x = tf.keras.layers.Embedding(input_dim=5000, output_dim=64)(text)
        x = tf.keras.layers.LSTM(128)(x)
        x = tf.keras.layers.Dropout(0.5)(x)

        emoji = tf.keras.layers.Dense(len(emojis), activation="sigmoid", name="emoji")(x)
        sentiment = tf.keras.layers.Dense(3, activation="sigmoid", name="sentiment")(x)

        model = tf.keras.Model(text, [emoji, sentiment])

        model.compile("RMSprop",
                  loss={'sentiment': "binary_crossentropy", "emoji": "binary_crossentropy"},
                  loss_weights={"sentiment":0.5, "emoji": 0.5})

        return model
        
    def _build_dummy_model(self):
        """Build a simple dummy model for testing and CI environments."""
        from types import SimpleNamespace
        
        class DummyModel:
            def predict(self, x):
                """Return dummy predictions for testing."""
                import numpy as np
                # Return dummy emoji probabilities and sentiment
                emoji_scores = np.ones((1, len(emojis))) * 0.5
                sentiment = np.array([[0.7]])
                return emoji_scores, sentiment
                
            def save(self, path):
                """Dummy save method."""
                pass
                
        return DummyModel()

    def _load_model(self):
        tf = self._get_tf()
        return tf.keras.models.load_model(self.model_path)

    def _set_baseline(self):
        tweet = Tweet("")
        x = tweet.x.reshape(1, -1)
        scores, sentiment = self._model.predict(x)
        self.baseline = scores

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
        x = tweet.x.reshape(1, -1)

        try:
            scores, sentiment = self._model.predict(x)

            if normalize:
                scores /= self.baseline
        except Exception as e:
            logging.error("Failed on tweet: %s. Error: %s", text, str(e))
            scores = self.baseline
            sentiment = np.array([[0.0]])


        scores = [float(s) for s in scores[0, :]]
        scores = dict(zip(emojis, scores))
        sentiment = float(sentiment[0, 0])
        return {"emoji":scores, "sentiment": sentiment}
