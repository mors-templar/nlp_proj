import textblob as tb
import vaderSentiment as vader

def get_user_sentiment(text):
    tb_score = TextBlob(text).sentiment.polarity
    vader_analyser = vader.vaderSentiment.SentimentIntensityAnalyzer()
    v_scores = vader_analyser.polarity_scores(text)
    v_cscores = v_scores["compound"]
    
    avg_score = (v_cscores + tb_scores) / 2
    
    if (avg_score > 0.15):
        sentiment = "positive"
    elif (avg_score < -0.15):
        sentiment = "negative"
    else:
        sentiment = "neutral"
    
    return avg_score , sentiment
        
    