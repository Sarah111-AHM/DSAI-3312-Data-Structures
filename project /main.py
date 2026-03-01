"""
main.py
النقطة الرئيسية للبرنامج: واجهة تفاعلية تعرض القائمة وتنفذ الخيارات
"""

import os
from text_processor import TextProcessor
from features import Trie, NGramPredictor, SpellChecker, SentimentAnalyzer
import utils

def load_initial_text():
    """تطلب من المستخدم إدخال النص إما مباشرة أو من ملف."""
    print("=== Smart Text Analyzer ===")
    while True:
        choice = input("هل تريد تحميل النص من ملف (f) أم إدخاله مباشرة (d)؟ [f/d]: ").strip().lower()
        if choice == 'f':
            path = input("أدخل مسار الملف: ").strip()
            if not os.path.exists(path):
                print("الملف غير موجود. حاول مرة أخرى.")
                continue
            try:
                raw_text = utils.load_file(path)
                print("تم تحميل النص من الملف بنجاح.")
                return raw_text
            except Exception as e:
                print(f"خطأ في قراءة الملف: {e}")
        elif choice == 'd':
            print("أدخل النص (عند الانتهاء اكتب $$END_TEXT$$ في سطر جديد):")
            lines = []
            while True:
                line = input()
                if line.strip() == "$$END_TEXT$$":
                    break
                lines.append(line)
            raw_text = '\n'.join(lines)
            return raw_text
        else:
            print("اختيار غير صالح، حاول مرة أخرى.")

def display_menu():
    print("\n--- القائمة الرئيسية ---")
    print("1. إحصائيات الكلمات")
    print("2. إحصائيات الحروف")
    print("3. بحث عن كلمة")
    print("4. استبدال كلمة")
    print("5. الإكمال التلقائي (Autocomplete)")
    print("6. توقع الكلمة التالية")
    print("7. اقتراح تصحيح إملائي")
    print("8. تحليل المشاعر")
    print("0. خروج")
    return input("اختر رقم الخيار: ").strip()

def main():
    raw_text = load_initial_text()
    processor = TextProcessor(raw_text)

    # بناء الميزات الذكية باستخدام بيانات المعالج
    trie = Trie()
    for w in processor.unique_words:
        trie.insert(w)

    predictor = NGramPredictor(processor.words)

    spell_checker = SpellChecker(processor.unique_words)

    # تأكد من وجود ملف lexicon
    lexicon_path = 'data/sentiment_lexicon.csv'
    if not os.path.exists(lexicon_path):
        print("تحذير: ملف lexicon غير موجود. سيتم إنشاء ملف افتراضي.")
        # يمكن إنشاء ملف بسيط
        os.makedirs('data', exist_ok=True)
        with open(lexicon_path, 'w', encoding='utf-8') as f:
            f.write("good,positive\nbad,negative\nhappy,positive\nsad,negative\n")
    sentiment = SentimentAnalyzer(lexicon_path)

    while True:
        choice = display_menu()

        if choice == '0':
            print("وداعاً!")
            break

        elif choice == '1':  # إحصائيات الكلمات
            total = len(processor.words)
            unique = len(processor.unique_words)
            print(f"\nإجمالي عدد الكلمات: {total}")
            print(f"عدد الكلمات الفريدة: {unique}")
            top = input("عرض أكثر الكلمات تكراراً؟ أدخل عدداً (أو اضغط Enter للتخطي): ").strip()
            if top.isdigit():
                top_n = int(top)
                freqs = processor.get_word_frequencies(top_n)
                for word, count in freqs:
                    print(f"  {word}: {count}")

        elif choice == '2':  # إحصائيات الحروف
            chars = processor.get_char_frequencies()
            total_chars = sum(chars.values())
            print(f"\nإجمالي عدد الحروف (بدون مسافات): {total_chars}")
            print("تكرار كل حرف:")
            for ch, count in sorted(chars.items()):
                print(f"  '{ch}': {count}")

        elif choice == '3':  # بحث عن كلمة
            word = input("أدخل الكلمة للبحث عنها: ").strip()
            results = processor.search_word(word)
            if results:
                print(f"تم العثور على '{word}' في {len(results)} موضع:")
                for sent, wpos in results:
                    print(f"  الجملة {sent}, الكلمة رقم {wpos}")
            else:
                print("لم يتم العثور على الكلمة.")

        elif choice == '4':  # استبدال كلمة
            old = input("أدخل الكلمة المراد استبدالها: ").strip()
            new = input("أدخل الكلمة الجديدة: ").strip()
            confirm = input(f"هل أنت متأكد من استبدال كل '{old}' بـ '{new}'؟ (نعم/لا): ").strip().lower()
            if confirm in ['نعم', 'y', 'yes']:
                success = processor.replace_word(old, new)
                if success:
                    print("تم الاستبدال بنجاح.")
                    # تحديث الهياكل الذكية (أعد بناءها)
                    trie = Trie()
                    for w in processor.unique_words:
                        trie.insert(w)
                    predictor = NGramPredictor(processor.words)
                    spell_checker = SpellChecker(processor.unique_words)
                else:
                    print("الكلمة غير موجودة في النص.")
            else:
                print("تم إلغاء العملية.")

        elif choice == '5':  # Autocomplete
            prefix = input("أدخل بادئة الكلمة: ").strip().lower()
            suggestions = trie.autocomplete(prefix)
            if suggestions:
                print("اقتراحات:", ', '.join(suggestions[:10]))
            else:
                print("لا توجد اقتراحات.")

        elif choice == '6':  # Next word prediction
            word = input("أدخل كلمة: ").strip().lower()
            predictions = predictor.predict(word)
            if predictions:
                print("الكلمات التالية المحتملة:")
                for w, count in predictions:
                    print(f"  {w} (تكررت {count} مرة)")
            else:
                print("لا توجد توقعات.")

        elif choice == '7':  # Spell suggestion
            word = input("أدخل كلمة للتدقيق الإملائي: ").strip().lower()
            suggestions = spell_checker.suggest(word)
            if suggestions:
                print("اقتراحات:", ', '.join(suggestions))
            else:
                print("الكلمة صحيحة أو لا توجد اقتراحات.")

        elif choice == '8':  # Sentiment analysis
            sentence = input("أدخل جملة لتحليل مشاعرها (أو اضغط Enter لتحليل النص كاملاً): ").strip()
            if not sentence:
                text_to_analyze = processor.clean_text
            else:
                text_to_analyze = sentence
            mood = sentiment.analyze(text_to_analyze)
            print(f"المشاعر المتوقعة: {mood}")

        else:
            print("اختيار غير صالح، حاول مرة أخرى.")

        input("\nاضغط Enter للعودة إلى القائمة...")

if __name__ == '__main__':
    main()
