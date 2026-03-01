
import os
from pathlib import Path

BASE_DIR = Path(__file__).parent

DATA_DIR = BASE_DIR / "data"
SENTIMENT_LEXICON_PATH = DATA_DIR / "sentiment_lexicon.csv"
STOPWORDS_PATH = DATA_DIR / "stopwords.txt"

DATA_DIR.mkdir(exist_ok=True)
