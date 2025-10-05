import sys
import pickle
import json
import nltk
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer
import string
import os
import warnings

# Suppress sklearn version warnings in production
if os.environ.get('NODE_ENV') == 'production':
    warnings.filterwarnings('ignore', category=UserWarning)
    warnings.filterwarnings('ignore', message='.*InconsistentVersionWarning.*')

# Download required NLTK data
try:
    stopwords.words('english')
except LookupError:
    nltk.download('stopwords')

try:
    nltk.word_tokenize("test")
except LookupError:
    nltk.download('punkt')

def transform_text(text):
    """
    Text preprocessing function - same as used in training
    """
    ps = PorterStemmer()
    text = text.lower()
    text = nltk.word_tokenize(text)
    y = []
    for token in text:
        # keep only alphanumeric tokens
        if token.isalnum():
            if token not in stopwords.words('english') and token not in string.punctuation:
                stemmed = ps.stem(token)
                y.append(stemmed)
    return " ".join(y)

def main():
    try:
        # Get text from command line argument
        if len(sys.argv) < 2:
            raise ValueError("No text provided")
        
        text = sys.argv[1]
        
        # Get the directory of this script
        script_dir = os.path.dirname(os.path.abspath(__file__))
        model_dir = os.path.join(script_dir, 'models')
        
        # Load the trained models
        model_path = os.path.join(model_dir, 'model.pkl')
        vectorizer_path = os.path.join(model_dir, 'vectorizer.pkl')
        
        with open(model_path, 'rb') as f:
            model = pickle.load(f)
        
        with open(vectorizer_path, 'rb') as f:
            vectorizer = pickle.load(f)
        
        # Preprocess the text
        transformed_text = transform_text(text)
        
        # Vectorize the text
        text_vector = vectorizer.transform([transformed_text])
        
        # Make prediction
        prediction = model.predict(text_vector)[0]
        probability = model.predict_proba(text_vector)[0]
        
        # Prepare result
        result = {
            "original_text": text,
            "transformed_text": transformed_text,
            "prediction": "spam" if prediction == 1 else "ham",
            "is_spam": bool(prediction),
            "confidence": {
                "ham": float(probability[0]),
                "spam": float(probability[1])
            },
            "confidence_percentage": {
                "ham": f"{probability[0]*100:.2f}%",
                "spam": f"{probability[1]*100:.2f}%"
            }
        }
        
        # Output result as JSON
        print(json.dumps(result))
        
    except Exception as e:
        error_result = {
            "error": True,
            "message": str(e),
            "original_text": text if 'text' in locals() else ""
        }
        print(json.dumps(error_result))
        sys.exit(1)

if __name__ == "__main__":
    main()