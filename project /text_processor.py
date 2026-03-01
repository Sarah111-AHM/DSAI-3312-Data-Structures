"""
text_processor.py
معالجة النص وتخزينه في هياكل بيانات مناسبة
"""

from collections import Counter
from utils import clean_text, split_sentences

class TextProcessor:
    def __init__(self, raw_text):
        self.raw_text = raw_text
        self.clean_text = clean_text(raw_text)
        # قائمة بكل الكلمات
        self.words = self.clean_text.split()
        # قائمة الجمل (كل جملة نص)
        self.sentences = split_sentences(self.clean_text)
        # قائمة الجمل حيث كل جملة هي قائمة كلمات (للبحث الدقيق)
        self.sentence_words = [s.split() for s in self.sentences]

        # إحصائيات أولية باستخدام Counter
        self.word_counts = Counter(self.words)
        self.unique_words = set(self.words)
        # عد الحروف بدون مسافات
        text_no_spaces = self.clean_text.replace(' ', '')
        self.char_counts = Counter(text_no_spaces)

    def get_word_frequencies(self, top_n=None):
        """إرجاع ترددات الكلمات. إذا أعطي top_n يرجع أكثر n تكراراً."""
        if top_n:
            return self.word_counts.most_common(top_n)
        return dict(self.word_counts)

    def get_char_frequencies(self):
        return dict(self.char_counts)

    def search_word(self, word):
        """
        البحث عن كلمة في النص.
        يعيد قائمة tuples (رقم الجملة, رقم الكلمة في الجملة) (تبدأ من 1)
        """
        word = word.lower()
        results = []
        for sent_idx, sent in enumerate(self.sentence_words):
            for word_idx, w in enumerate(sent):
                if w == word:
                    results.append((sent_idx + 1, word_idx + 1))
        return results

    def replace_word(self, old, new):
        """
        استبدال كل تكرارات old بكلمة new في جميع الهياكل.
        تعيد True إذا تم أي استبدال، False إذا لم توجد الكلمة.
        """
        old = old.lower()
        new = new.lower()
        replaced = False

        # استبدال في قائمة الكلمات المسطحة
        for i, w in enumerate(self.words):
            if w == old:
                self.words[i] = new
                replaced = True

        if not replaced:
            return False

        # إعادة بناء النص النظيف من قائمة الكلمات المحدثة
        self.clean_text = ' '.join(self.words)

        # إعادة بناء الجمل
        self.sentences = split_sentences(self.clean_text)
        self.sentence_words = [s.split() for s in self.sentences]

        # تحديث الإحصائيات
        self.word_counts = Counter(self.words)
        self.unique_words = set(self.words)

        # تحديث عد الحروف
        text_no_spaces = self.clean_text.replace(' ', '')
        self.char_counts = Counter(text_no_spaces)

        return True
