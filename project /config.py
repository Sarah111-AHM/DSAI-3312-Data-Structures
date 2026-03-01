# config.py
import os
from pathlib import Path

BASE_DIR = Path(__file__).parent

# للـ Vercel، المسار مختلف
DATA_DIR = BASE_DIR / "data"
SENTIMENT_LEXICON_PATH = DATA_DIR / "sentiment_lexicon.csv"

# تأكد من وجود المجلد
DATA_DIR.mkdir(exist_ok=True)
