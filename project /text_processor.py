# text_processor.py
from collections import Counter
from typing import List, Dict, Tuple, Optional
import utils

class TextProcessor:
    def __init__(self, raw_text: str):
        self.raw_text = raw_text
        self.clean_text = utils.clean_text(raw_text)
        self.words: List[str] = self.clean_text.split()
        self.sentences: List[str] = utils.split_sentences(self.clean_text)
        self.sentence_words: List[List[str]] = [s.split() for s in self.sentences]

        # إحصائيات
        self.word_counts: Counter = Counter(self.words)
        self.unique_words: set = set(self.words)
        text_no_spaces = self.clean_text.replace(' ', '')
        self.char_counts: Counter = Counter(text_no_spaces)

    def get_word_stats(self) -> Tuple[int, int]:
        """إرجاع (إجمالي الكلمات, الكلمات الفريدة)"""
        return len(self.words), len(self.unique_words)

    def get_top_words(self, n: int = 10) -> List[Tuple[str, int]]:
        return self.word_counts.most_common(n)

    def get_char_stats(self) -> Dict[str, int]:
        return dict(self.char_counts)

    def search_word(self, word: str) -> List[Tuple[int, int]]:
        """
        البحث عن كلمة. يرجع قائمة (رقم الجملة, رقم الكلمة في الجملة)
        """
        word = word.lower()
        results = []
        for sent_idx, sent in enumerate(self.sentence_words):
            for word_idx, w in enumerate(sent):
                if w == word:
                    results.append((sent_idx + 1, word_idx + 1))
        return results

    def replace_word(self, old: str, new: str) -> bool:
        """
        استبدال كل تكرارات old بكلمة new.
        تُعيد True إذا تم الاستبدال.
        """
        old = old.lower()
        new = new.lower()
        replaced = False

        for i, w in enumerate(self.words):
            if w == old:
                self.words[i] = new
                replaced = True

        if not replaced:
            return False

        # إعادة بناء النص والهياكل الأخرى
        self.clean_text = ' '.join(self.words)
        self.sentences = utils.split_sentences(self.clean_text)
        self.sentence_words = [s.split() for s in self.sentences]
        self.word_counts = Counter(self.words)
        self.unique_words = set(self.words)
        text_no_spaces = self.clean_text.replace(' ', '')
        self.char_counts = Counter(text_no_spaces)

        return True
