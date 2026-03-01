# utils.py
import re
import string
from pathlib import Path
from typing import List, Dict

def clean_text(text: str, remove_punct: bool = True) -> str:
    """
    تنظيف النص: خفض الحالة، إزالة علامات الترقيم اختيارياً، توحيد المسافات.
    """
    text = text.lower()
    if remove_punct:
        text = text.translate(str.maketrans('', '', string.punctuation))
    text = re.sub(r'\s+', ' ', text).strip()
    return text

def split_sentences(text: str) -> List[str]:
    """
    تقسيم النص إلى جمل باستخدام علامات . ! ؟
    """
    sentences = re.split(r'[.!?]+', text)
    return [s.strip() for s in sentences if s.strip()]

def load_file(filepath: Path) -> str:
    """
    قراءة محتوى ملف نصي مع ترميز utf-8.
    """
    with open(filepath, 'r', encoding='utf-8') as f:
        return f.read()

def load_sentiment_lexicon(filepath: Path) -> Dict[str, str]:
    """
    تحميل قاموس المشاعر من ملف CSV: كل سطر: كلمة,قطبية.
    """
    lexicon = {}
    if not filepath.exists():
        # إنشاء ملف افتراضي إذا لم يكن موجوداً
        _create_default_lexicon(filepath)
    with open(filepath, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith('#'):
                continue
            parts = line.split(',')
            if len(parts) >= 2:
                word = parts[0].strip().lower()
                polarity = parts[1].strip().lower()
                lexicon[word] = polarity
    return lexicon

def _create_default_lexicon(filepath: Path):
    """إنشاء ملف lexicon افتراضي."""
    default_data = """good,positive
great,positive
excellent,positive
bad,negative
terrible,negative
awful,negative
happy,positive
sad,negative
ok,neutral
fine,neutral
"""
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(default_data)
