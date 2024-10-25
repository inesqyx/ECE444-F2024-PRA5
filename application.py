# Codegen by ChatGPT
# Prompt used: I need a web front that have a input box for user to input the news they want to check, 
# Pass the news to model to predict and then return to the front to tell the user whether it is a fake news
from flask import Flask, request, render_template
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
import pickle

application = Flask(__name__)

def load_model():
    with open('basic_classifier.pkl', 'rb') as model_file:
        model = pickle.load(model_file)
    with open('count_vectorizer.pkl', 'rb') as vectorizer_file:
        vectorizer = pickle.load(vectorizer_file)
    return model, vectorizer

model, vectorizer = load_model()

@application.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        news_text = request.form.get('news_text')
        prediction = model.predict(vectorizer.transform([news_text]))[0]
        return render_template('index.html', result=prediction)
    return render_template('index.html')

if __name__ == '__main__':
    application.run()
