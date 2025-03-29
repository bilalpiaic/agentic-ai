import nltk
from nltk.sentiment import SentimentIntensityAnalyzer
nltk.download('vader_lexicon')

sia = SentimentIntensityAnalyzer()
text = "NLTK is bad for natural language processing!"
sentiment = sia.polarity_scores(text)

print(sentiment) 