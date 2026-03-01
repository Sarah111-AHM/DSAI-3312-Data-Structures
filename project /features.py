"""
features.py
الميزات الذكية: إكمال تلقائي، توقع الكلمة التالية، اقتراح إملائي، تحليل المشاعر
"""

from collections import defaultdict, Counter
import utils

# ---------- 1. Trie for Autocomplete ----------
class TrieNode:
    __slots__ = ('children', 'is_end')
    def __init__(self):
        self.children = {}
        self.is_end = False

class Trie:
    def __init__(self):
        self.root = TrieNode()

    def insert(self, word):
        node = self.root
        for ch in word:
            if ch not in node.children:
                node.children[ch] = TrieNode()
            node = node.children[ch]
        node.is_end = True

    def _find_node(self, prefix):
        node = self.root
        for ch in prefix:
            if ch not in node.children:
                return None
            node = node.children[ch]
        return node

    def _collect_words(self, node, prefix, result):
        if node.is_end:
            result.append(prefix)
        for ch, child in node.children.items():
            self._collect_words(child, prefix + ch, result)

    def autocomplete(self, prefix):
        """إرجاع قائمة بالكلمات التي تبدأ بالبادئة المعطاة."""
        node = self._find_node(prefix)
        if not node:
            return []
        results = []
        self._collect_words(node, prefix, results)
        return results


# ---------- 2. N-Gram Predictor (Bigram) ----------
class NGramPredictor:
    def __init__(self, words):
        # bigrams: {word1: Counter({word2: count, ...})}
        self.bigrams = defaultdict(Counter)
        self._build(words)

    def _build(self, words):
        for i in range(len(words) - 1):
            w1 = words[i]
            w2 = words[i+1]
            self.bigrams[w1][w2] += 1

    def predict(self, word, top_n=3):
        """يتوقع الكلمات التالية المحتملة لكلمة معينة."""
        if word not in self.bigrams:
            return []
        # يرجع قائمة tuples (الكلمة, التكرار)
        return self.bigrams[word].most_common(top_n)


# ---------- 3. Spell Checker / Suggester ----------
def _edits1(word):
    """توليد جميع الكلمات التي تبعد مسافة تحرير واحدة عن الكلمة المدخلة."""
    letters = 'abcdefghijklmnopqrstuvwxyz'
    splits = [(word[:i], word[i:]) for i in range(len(word) + 1)]
    deletes = [L + R[1:] for L, R in splits if R]
    transposes = [L + R[1] + R[0] + R[2:] for L, R in splits if len(R) > 1]
    replaces = [L + c + R[1:] for L, R in splits if R for c in letters]
    inserts = [L + c + R for L, R in splits for c in letters]
    return set(deletes + transposes + replaces + inserts)

def _edits2(word):
    """توليد الكلمات التي تبعد مسافتين تحرير."""
    return set(e2 for e1 in _edits1(word) for e2 in _edits1(e1))

class SpellChecker:
    def __init__(self, vocabulary):
        self.vocab = vocabulary  # set of words

    def suggest(self, word, top_n=5):
        word = word.lower()
        if word in self.vocab:
            return []  # الكلمة صحيحة

        # اقتراحات بمسافة 1
        suggestions = _edits1(word) & self.vocab
        if len(suggestions) < top_n:
            # أضف اقتراحات بمسافة 2
            suggestions.update(_edits2(word) & self.vocab)

        # حول إلى قائمة واختر أفضل top_n (حسب الترتيب الأبجدي أو أي معيار)
        # يمكن تحسين الترتيب باستخدام التكرارات، لكن هنا نبقيها بسيطة
        suggestions = list(suggestions)
        suggestions.sort()  # ترتيب أبجدي
        return suggestions[:top_n]


# ---------- 4. Sentiment Analyzer ----------
class SentimentAnalyzer:
    def __init__(self, lexicon_file):
        self.lexicon = utils.load_sentiment_lexicon(lexicon_file)

    def analyze(self, text):
        words = utils.clean_text(text).split()
        scores = {'positive': 0, 'negative': 0, 'neutral': 0}
        for w in words:
            if w in self.lexicon:
                scores[self.lexicon[w]] += 1
        # تحديد النتيجة الأكثر تكراراً
        if scores['positive'] > scores['negative']:
            return 'positive'
        elif scores['negative'] > scores['positive']:
            return 'negative'
        else:
            return 'neutral'
