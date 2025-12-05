import random

from models import db
from .emojis import emojis, positive_emojis, negative_emojis


class Vector(list):
    """Lightweight list wrapper that mimics the shape attribute of numpy arrays."""

    def __init__(self, values):
        super().__init__(values)

    @property
    def shape(self):
        return (len(self),)


class Tweet(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    raw_tweet = db.Column(db.String(140))

    def __init__(self, raw_tweet):
        self.raw_tweet = raw_tweet or ""

    @property
    def text(self):
        text = self.raw_tweet
        for e in emojis:
            text = text.replace(e, "")
        return text

    @property
    def emojis(self):
        return [e for e in emojis if e in self.raw_tweet]

    @property
    def sentiment(self):
        scores = [0.0, 0.0, 0.0]
        if self.emojis:
            choice = random.choice(self.emojis)
            if choice in positive_emojis:
                scores[0] = 1.0
            elif choice in negative_emojis:
                scores[2] = 1.0
            else:
                scores[1] = 1.0
        return Vector(scores)

    @property
    def x(self):
        """Return a 140-length vector of integer character codes."""
        values = [ord(c) % 5000 for c in self.text]
        if len(values) < 140:
            padding = [0] * (140 - len(values))
            values = padding + values
        return Vector(values[:140])

    @property
    def y(self):
        values = [0.0] * len(emojis)
        for e in self.emojis:
            try:
                idx = emojis.index(e)
            except ValueError:
                continue
            values[idx] = 1.0
        return Vector(values)
