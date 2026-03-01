# features/spell.py
from typing import Set, List

def _edits1(word: str) -> Set[str]:
    """توليد الكلمات بمسافة تحرير 1."""
    letters = 'abcdefghijklmnopqrstuvwxyz'
    splits = [(word[:i], word[i:]) for i in range(len(word) + 1)]
    deletes = [L + R[1:] for L, R in splits if R]
    transposes = [L + R[1] + R[0] + R[2:] for L, R in splits if len(R) > 1]
    replaces = [L + c + R[1:] for L, R in splits if R for c in letters]
    inserts = [L + c + R for L, R in splits for c in letters]
    return set(deletes + transposes + replaces + inserts)

def _edits2(word: str) -> Set[str]:
    """توليد الكلمات بمسافة تحرير 2."""
    return {e2 for e1 in _edits1(word) for e2 in _edits1(e1)}

class SpellSuggestionFeature:
    def __init__(self, vocabulary: Set[str]):
        self.vocab = vocabulary

    def suggest(self, word: str, top_n: int = 5) -> List[str]:
        word = word.lower()
        if word in self.vocab:
            return []  # صحيحة

        suggestions = _edits1(word) & self.vocab
        if len(suggestions) < top_n:
            suggestions.update(_edits2(word) & self.vocab)

        # ترتيب أبجدي (يمكن تحسينه لاحقاً بالتردد)
        return sorted(suggestions)[:top_n]
