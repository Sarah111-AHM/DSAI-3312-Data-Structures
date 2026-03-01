# features/prediction.py
from data_structures.ngram import NGramPredictor

class NextWordPredictionFeature:
    def __init__(self, words):
        self.predictor = NGramPredictor(words, n=2)  # bigram

    def predict(self, word: str) -> list:
        return self.predictor.predict([word])
