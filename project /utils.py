"""
utils.py
دوال مساعدة لمعالجة النصوص
"""

import re
import string

def clean_text(text):
    """
    تنظيف النص: خفض حالة الأحرف، إزالة علامات الترقيم، توحيد المسافات.
    """
    # خفض الحالة
    text = text.lower()
    # إزالة علامات الترقيم (نحتفظ ببعضها إذا لزم، لكن هنا نزيل الكل)
    text = text.translate(str.maketrans('', '', string.punctuation))
    # استبدال المسافات المتعددة بمسافة واحدة
    text = re.sub(r'\s+', ' ', text).strip()
    return text

def split_sentences(text):
    """
    تقسيم النص إلى جمل بناءً على . ! ؟
    """
    # نمط بسيط: أي نقطة أو علامة تعجب أو استفهام متبوعة بمسافة أو نهاية سطر
    sentences = re.split(r'[.!?]+', text)
    # إزالة الفراغات الزائدة وتجاهل الجمل الفارغة
    return [s.strip() for s in sentences if s.strip()]

def load_file(filepath):
    """
    قراءة محتوى ملف نصي مع ترميز utf-8.
    """
    with open(filepath, 'r', encoding='utf-8') as f:
        return f.read()

def load_sentiment_lexicon(filepath):
    """
    تحميل قاموس المشاعر من ملف CSV بسيط.
    تنسيق كل سطر: كلمة,قطبية (positive/negative/neutral)
    """
    lexicon = {}
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
