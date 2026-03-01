# api/index.py
from flask import Flask, request, jsonify, render_template_string
import sys
import os
from pathlib import Path

# إضافة المسار الرئيسي
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

# استيراد الكلاسز القديمة كما هي
from text_processor import TextProcessor
from features.autocomplete import AutocompleteFeature
from features.prediction import NextWordPredictionFeature
from features.spell import SpellSuggestionFeature
from features.sentiment import SentimentFeature

app = Flask(__name__)

# صفحة HTML بسيطة
HTML_TEMPLATE = '''
<!DOCTYPE html>
<html dir="rtl">
<head>
    <title>Smart Text Analyzer</title>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <style>
        body { font-family: Arial; margin: 20px; background: #f5f5f5; }
        .container { max-width: 800px; margin: auto; background: white; padding: 20px; border-radius: 10px; box-shadow: 0 0 10px rgba(0,0,0,0.1); }
        textarea { width: 100%; height: 200px; margin: 10px 0; padding: 10px; }
        button { background: #007bff; color: white; border: none; padding: 10px 20px; border-radius: 5px; cursor: pointer; }
        .result { margin-top: 20px; padding: 10px; background: #e9ecef; border-radius: 5px; }
    </style>
</head>
<body>
    <div class="container">
        <h1>📊 Smart Text Analyzer</h1>
        
        <textarea id="textInput" placeholder="أدخل النص هنا..."></textarea><br>
        <button onclick="analyze()">تحليل النص</button>
        
        <div id="results" class="result"></div>
    </div>

    <script>
        function analyze() {
            const text = document.getElementById('textInput').value;
            if (!text) {
                alert('الرجاء إدخال نص');
                return;
            }

            const resultsDiv = document.getElementById('results');
            resultsDiv.innerHTML = 'جاري التحليل...';

            fetch('/analyze', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({text: text})
            })
            .then(res => res.json())
            .then(data => {
                let html = '<h3>النتائج:</h3>';
                html += '<ul>';
                html += '<li>عدد الكلمات: ' + data.word_count + '</li>';
                html += '<li>كلمات فريدة: ' + data.unique_words + '</li>';
                html += '<li>عدد الحروف: ' + data.char_count + '</li>';
                html += '<li>المشاعر: ' + data.sentiment + '</li>';
                html += '</ul>';
                
                html += '<h4>أكثر 5 كلمات تكراراً:</h4><ul>';
                data.top_words.forEach(w => {
                    html += '<li>' + w[0] + ': ' + w[1] + '</li>';
                });
                html += '</ul>';
                
                resultsDiv.innerHTML = html;
            });
        }
    </script>
</body>
</html>
'''

@app.route('/')
def home():
    return render_template_string(HTML_TEMPLATE)

@app.route('/analyze', methods=['POST'])
def analyze():
    data = request.json
    text = data.get('text', '')
    
    # استخدام الكلاسز القديمة كما هي
    processor = TextProcessor(text)
    sentiment = SentimentFeature('data/sentiment_lexicon.csv')
    
    return jsonify({
        'word_count': len(processor.words),
        'unique_words': len(processor.unique_words),
        'char_count': sum(processor.char_counts.values()),
        'top_words': processor.get_top_words(5),
        'sentiment': sentiment.analyze(text)
    })

# هذا السطر ضروري لـ Vercel
handler = app
