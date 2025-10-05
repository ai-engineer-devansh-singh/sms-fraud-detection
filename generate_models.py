#!/usr/bin/env python3
"""
Generate ML models for SMS spam detection
"""

import pandas as pd
import numpy as np
import nltk
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer
import string
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, precision_score
import pickle
import os

# Download NLTK data
try:
    stopwords.words('english')
except LookupError:
    nltk.download('stopwords')

try:
    nltk.word_tokenize("test")
except LookupError:
    nltk.download('punkt')

def transform_text(text):
    ps = PorterStemmer()
    text = text.lower()
    text = nltk.word_tokenize(text)
    y = []
    for token in text:
        if token.isalnum():
            if token not in stopwords.words('english') and token not in string.punctuation:
                stemmed = ps.stem(token)
                y.append(stemmed)
    return " ".join(y)

def main():
    print("🔥 Generating SMS Spam Detection Models...")
    
    # Load data
    print("📚 Loading data...")
    df = pd.read_csv('notebook/spam.csv', encoding='cp1252')
    
    # Data cleaning
    print("🧹 Cleaning data...")
    df.drop(columns=['Unnamed: 2', 'Unnamed: 3', 'Unnamed: 4'], inplace=True)
    df.rename(columns={'v1': 'target', 'v2': 'text'}, inplace=True)
    
    # Label encoding
    from sklearn.preprocessing import LabelEncoder
    le = LabelEncoder()
    df['target'] = le.fit_transform(df['target'])
    
    # Remove duplicates
    df = df.drop_duplicates(keep='first')
    
    # Text preprocessing
    print("📝 Preprocessing text...")
    df['transformed_text'] = df['text'].apply(transform_text)
    
    # Vectorization
    print("🔢 Vectorizing text...")
    tfidf = TfidfVectorizer(max_features=3000)
    X = tfidf.fit_transform(df['transformed_text']).toarray()
    y = df['target'].values
    
    # Train-test split
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=2)
    
    # Train model
    print("🤖 Training model...")
    model = MultinomialNB()
    model.fit(X_train, y_train)
    
    # Evaluate
    y_pred = model.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)
    precision = precision_score(y_test, y_pred)
    
    print(f"✅ Model trained successfully!")
    print(f"📊 Accuracy: {accuracy:.4f}")
    print(f"📊 Precision: {precision:.4f}")
    
    # Save models
    print("💾 Saving models...")
    os.makedirs('models', exist_ok=True)
    
    with open('models/model.pkl', 'wb') as f:
        pickle.dump(model, f)
    
    with open('models/vectorizer.pkl', 'wb') as f:
        pickle.dump(tfidf, f)
    
    print("✅ Models saved to models/ directory")
    
    # Test the saved models
    print("🧪 Testing saved models...")
    with open('models/model.pkl', 'rb') as f:
        loaded_model = pickle.load(f)
    
    with open('models/vectorizer.pkl', 'rb') as f:
        loaded_vectorizer = pickle.load(f)
    
    # Test prediction
    test_text = "Congratulations! You have won $1000. Click here to claim now!"
    transformed_test = transform_text(test_text)
    test_vector = loaded_vectorizer.transform([transformed_test])
    prediction = loaded_model.predict(test_vector)[0]
    probability = loaded_model.predict_proba(test_vector)[0]
    
    print(f"🧪 Test prediction: {'SPAM' if prediction == 1 else 'HAM'}")
    print(f"🧪 Confidence: {max(probability):.4f}")
    
    print("🎉 Model generation complete!")

if __name__ == "__main__":
    main()