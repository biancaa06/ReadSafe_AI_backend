import joblib
import numpy as np
import pandas as pd
from textstat import flesch_reading_ease
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
import string
from tokenizer import identity_tokenizer

# Load models
nb_model = joblib.load("model/nb_model.pkl")
bagging_model = joblib.load("model/bagging_model.pkl")
vectorizer = joblib.load("model/tfidf_vectorizer.pkl")

stopwords_list = stopwords.words('english')
lemmatizer = WordNetLemmatizer()

def preprocess(text):
    text = text.lower()
    text = text.translate(str.maketrans('', '', string.punctuation))
    tokens = word_tokenize(text)
    tokens = [word for word in tokens if word not in stopwords_list]
    tokens = [lemmatizer.lemmatize(word) for word in tokens]
    return tokens

def predict_story_label(story_text):
    tokens = preprocess(story_text)
    flesch_score = flesch_reading_ease(story_text)
    vocab_div = len(set(tokens)) / len(tokens) if tokens else 0
    joined = ' '.join(tokens)

    X_nb = vectorizer.transform([joined])
    X_dt = pd.DataFrame([[flesch_score, vocab_div]], columns=["flesch_score", "vocab_diversity"])

    nb_probs = nb_model.predict_proba(X_nb)[0]
    dt_probs = bagging_model.predict_proba(X_dt)[0]

    nb_out = nb_model.classes_[nb_probs.argmax()]
    dt_out = bagging_model.classes_[dt_probs.argmax()]

    if dt_out == 3 or nb_out == 3:
        final_label = 3
        final_certainty = max(dt_probs[2], nb_probs[2])
    else:
        final_label = int(nb_out)
        final_certainty = nb_probs[nb_out - 1]

    return final_label, final_certainty
