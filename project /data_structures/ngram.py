# data_structures/ngram.py
from collections import defaultdict, Counter
from typing import List, Dict, Tuple

class NGramPredictor:
    def __init__(self, words: List[str], n: int = 2):
        """
        n: حجم n-gram (افتراضي 2 للـ bigram)
        """
        self.n = n
        self.model = defaultdict(Counter)
        self._build(words)

    def _build(self, words: List[str]) -> None:
        for i in range(len(words) - self.n + 1):
            context = tuple(words[i:i+self.n-1])  # الكلمات السابقة
            next_word = words[i+self.n-1]         # الكلمة التالية
            self.model[context][next_word] += 1

    def predict(self, context: List[str], top_n: int = 3) -> List[Tuple[str, int]]:
        """
        يتوقع الكلمات التالية المحتملة لسياق معين.
        context: قائمة الكلمات السابقة (يجب أن يكون طولها n-1)
        """
        key = tuple(context)
        if key not in self.model:
            return []
        return self.model[key].most_common(top_n)
