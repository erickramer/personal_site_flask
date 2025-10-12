import pytest
import json
from sentiment.ml import SentimentModel
from sentiment.models import Tweet

pytestmark = [pytest.mark.sentiment, pytest.mark.integration]

@pytest.fixture
def mock_sentiment_model(monkeypatch):
    """Mock the sentiment model to avoid loading the actual model."""
    class MockModel:
        def score(self, text, normalize=True):
            # Mock response that mimics the real model output structure
            return {
                "emoji": {
                    "😊": 0.9,  # Happy emoji scores high for positive text
                    "😢": 0.1   # Sad emoji scores low for positive text
                },
                "sentiment": 0.8  # High score for positive sentiment
            }
    
    # Apply the monkeypatch for testing
    monkeypatch.setattr("sentiment.ml.SentimentModel", MockModel)
    return MockModel()

def test_sentiment_route(client):
    """Test that the sentiment page loads correctly."""
    response = client.get('/sentiment')
    assert response.status_code == 200
    assert b'Tweet sentiment analyzer' in response.data

def test_sentiment_api_score(client, mock_sentiment_model):
    """Test the sentiment analysis API endpoint."""
    test_text = "I love this application!"
    response = client.post('/sentiment/api/score', 
                          data={"text": test_text})
    
    assert response.status_code == 200
    data = json.loads(response.data)

    # Check that the response has the expected structure
    assert "emoji" in data
    assert "sentiment" in data
    assert isinstance(data["sentiment"], (int, float))
    assert isinstance(data["emoji"], dict)

    # Validate the mocked sentiment scores
    assert data["sentiment"] == pytest.approx(0.8)
    assert data["emoji"]["😊"] == pytest.approx(0.9)
    assert data["emoji"]["😢"] == pytest.approx(0.1)

def test_tweet_model(session):
    """Test basic Tweet model functionality."""
    # Create a test tweet
    tweet = Tweet("Hello world! 😊")
    session.add(tweet)
    session.commit()
    
    # Test tweet properties
    assert "Hello world!" in tweet.text
    assert "😊" in tweet.emojis
    assert tweet.x.shape == (140,)  # Should be padded to 140 chars
    
    # Test retrieval
    retrieved = session.query(Tweet).filter_by(raw_tweet="Hello world! 😊").first()
    assert retrieved.raw_tweet == "Hello world! 😊"

def test_dummy_model_used_in_app_engine(monkeypatch, app):
    """Ensure we fall back to the dummy sentiment model on App Engine."""
    monkeypatch.setenv("GAE_ENV", "standard")

    with app.app_context():
        model = SentimentModel()
        result = model.score("Test tweet")

    monkeypatch.delenv("GAE_ENV", raising=False)

    assert "emoji" in result and "sentiment" in result
