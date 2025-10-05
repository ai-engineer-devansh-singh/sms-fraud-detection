from flask import Flask, render_template, request, jsonify
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

app = Flask(__name__)

# Global variables for the ML models
model = None
vectorizer = None
stemmer = PorterStemmer()

def ensure_nltk_data():
    """Ensure NLTK data is available, download if necessary"""
    import io
    import sys
    
    # Redirect stdout temporarily to capture download messages
    old_stdout = sys.stdout
    old_stderr = sys.stderr
    
    try:
        # Try to access stopwords
        stopwords.words('english')
    except LookupError:
        try:
            # Suppress download output
            sys.stdout = io.StringIO()
            sys.stderr = io.StringIO()
            nltk.download('stopwords', quiet=True)
        finally:
            sys.stdout = old_stdout
            sys.stderr = old_stderr
    
    try:
        # Try to access punkt tokenizer
        nltk.word_tokenize("test")
    except LookupError:
        try:
            # Suppress download output
            sys.stdout = io.StringIO()
            sys.stderr = io.StringIO()
            nltk.download('punkt', quiet=True)
        finally:
            sys.stdout = old_stdout
            sys.stderr = old_stderr

def load_models():
    """Load the ML models at startup"""
    global model, vectorizer
    
    # Get the directory of this script and find models
    script_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Try different possible locations for models directory
    possible_model_dirs = [
        os.path.join(script_dir, 'models'),  # Same directory as script
        os.path.join(os.path.dirname(script_dir), 'src', 'models'),  # ../src/models
        os.path.join(os.path.dirname(script_dir), 'models'),  # ../models
        os.path.join(script_dir, 'src', 'models'),  # ./src/models
    ]
    
    model_dir = None
    for possible_dir in possible_model_dirs:
        if os.path.exists(possible_dir):
            model_dir = possible_dir
            break
    
    if model_dir is None:
        raise FileNotFoundError(f"Model directory not found. Tried: {possible_model_dirs}")
    
    # Load the trained models
    model_path = os.path.join(model_dir, 'model.pkl')
    vectorizer_path = os.path.join(model_dir, 'vectorizer.pkl')
    
    if not os.path.exists(model_path):
        raise FileNotFoundError(f"Model file not found: {model_path}")
    if not os.path.exists(vectorizer_path):
        raise FileNotFoundError(f"Vectorizer file not found: {vectorizer_path}")
    
    with open(model_path, 'rb') as f:
        model = pickle.load(f)
    
    with open(vectorizer_path, 'rb') as f:
        vectorizer = pickle.load(f)
    
    print("✅ Models loaded successfully")

def transform_text(text):
    """Text preprocessing function - same as used in training"""
    text = text.lower()
    text = nltk.word_tokenize(text)
    y = []
    for token in text:
        # keep only alphanumeric tokens
        if token.isalnum():
            if token not in stopwords.words('english') and token not in string.punctuation:
                stemmed = stemmer.stem(token)
                y.append(stemmed)
    return " ".join(y)

def predict_spam(text):
    """Make a spam prediction for the given text"""
    if model is None or vectorizer is None:
        raise ValueError("Models not loaded")
    
    # Preprocess the text
    transformed_text = transform_text(text)
    
    # Vectorize the text
    text_vector = vectorizer.transform([transformed_text])
    
    # Make prediction
    prediction = model.predict(text_vector)[0]
    probability = model.predict_proba(text_vector)[0]
    
    return {
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

@app.route('/')
def index():
    """Serve the main page"""
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    """Handle prediction requests"""
    try:
        data = request.get_json()
        
        if not data or 'text' not in data:
            return jsonify({
                'error': True,
                'message': 'No text provided'
            }), 400
        
        text = data['text'].strip()
        if not text:
            return jsonify({
                'error': True,
                'message': 'Empty text provided'
            }), 400
        
        result = predict_spam(text)
        return jsonify(result)
        
    except Exception as e:
        return jsonify({
            'error': True,
            'message': str(e)
        }), 500

@app.route('/health')
def health():
    """Health check endpoint"""
    return jsonify({
        'status': 'OK',
        'message': 'SMS Spam Detection API is running',
        'models_loaded': model is not None and vectorizer is not None
    })

if __name__ == '__main__':
    try:
        print("🔥 Starting SMS Spam Detection Service...")
        
        # Initialize NLTK data
        print("📚 Ensuring NLTK data is available...")
        ensure_nltk_data()
        
        # Load ML models
        print("🤖 Loading ML models...")
        load_models()
        
        print("🚀 SMS Spam Detection Service is ready!")
        
        # Get port from environment (Render sets this)
        port = int(os.environ.get('PORT', 5000))
        
        # Run the app
        app.run(host='0.0.0.0', port=port, debug=False)
        
    except Exception as e:
        print(f"❌ Failed to start service: {e}")
        sys.exit(1)