from flask import Flask
from flask import render_template, request, redirect, flash, url_for
from transformers import pipeline, BertForSequenceClassification, AutoTokenizer
import numpy as np
import pandas as pd
from youtube import print_video_comment
import os
from dotenv import load_dotenv

load_dotenv(os.path.join(os.path.dirname(__file__), '..', '..', '.env'))

app = Flask(__name__)
app.secret_key = os.environ.get('APP_SECRET_KEY')

model_path = 'model/my_trained_model'
tokenizer = AutoTokenizer.from_pretrained(model_path)
model = BertForSequenceClassification.from_pretrained(model_path)
sentiment_pipeline = pipeline('text-classification', model=model, tokenizer=tokenizer)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/search')
def search():
    return render_template('search.html')

@app.route('/predict', methods=['GET', 'POST'])
def predict():
    if request.method == 'POST':
        input_text = request.form['input']
        print(input_text)
        if input_text == '':
            flash('1文字以上入力してください')
            return redirect(url_for('search'))
        text_list = input_text.splitlines()
        results = []
        for text in text_list:
            model_prediction = sentiment_pipeline(text)[0]
            label = model_prediction['label']
            text_label = [text, label]
            results.append(text_label)
        count_pos = np.sum(np.array(results) == 'positive')
        count_neg = np.sum(np.array(results) == 'negative')
        return render_template('predict.html', results=results, count_pos=count_pos, count_neg=count_neg)
    else:
        return render_template('predict.html')

@app.route('/searchYT')
def searchYT():
    return render_template('searchYT.html')

@app.route('/predictYT', methods=['GET', 'POST'])
def predictYT():
    if request.method == 'POST':
        text_data=[]
        video_id = request.form['video_id']
        no = 1
        print_video_comment(no, video_id, None, text_data)
        print(text_data)
        if text_data[0] == 'bad_id':
            flash('正しい video_id を入力してください')
            return redirect(url_for(('searchYT')))
        df = pd.DataFrame(text_data)
        text_list = df[2]
        results = []
        for text in text_list:
            try:
                model_prediction = sentiment_pipeline(text)[0]
            except RuntimeError:
                continue
            label = model_prediction['label']
            text_label = [text, label]
            results.append(text_label)
        print(results)
        count_pos = np.sum(np.array(results) == 'positive')
        count_neg = np.sum(np.array(results) == 'negative')
        print(count_pos, count_neg)
        return render_template('predictYT.html', results=results, count_pos=count_pos, count_neg=count_neg)
    else:
        return render_template('predictYT.html')