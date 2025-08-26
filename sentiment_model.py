from textblob import TextBlob
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

vader_analyzer = SentimentIntensityAnalyzer()


def get_user_sentiment(text):
    tb_score = TextBlob(text).sentiment.polarity

    v_scores = vader_analyzer.polarity_scores(text)
    v_cscore = v_scores["compound"]

    avg_score = (v_cscore + tb_score) / 2

    if avg_score > 0.15:
        sentiment = "Positive"
    elif avg_score < -0.15:
        sentiment = "Negative"
    else:
        sentiment = "Neutral"

    return avg_score, sentiment
