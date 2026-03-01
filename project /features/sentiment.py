# features/sentiment.py
from typing import Dict
import utils

class SentimentFeature:
    def __init__(self, lexicon_path):
        self.lexicon = utils.load_sentiment_lexicon(lexicon_path)

    def analyze(self, text: str) -> str:
        words = utils.clean_text(text).split()
        scores = {'positive': 0, 'negative': 0, 'neutral': 0}
        for w in words:
            polarity = self.lexicon.get(w)
            if polarity:
                scores[polarity] += 1
        if scores['positive'] > scores['negative']:
            return 'positive'
        elif scores['negative'] > scores['positive']:
            return 'negative'
        else:
            return 'neutral'
