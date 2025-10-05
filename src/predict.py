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

# Download required NLTK data with better error handling
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

# Initialize NLTK data
ensure_nltk_data()

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
        
        # Get the directory of this script and find models
        script_dir = os.path.dirname(os.path.abspath(__file__))
        
        # Try different possible locations for models directory
        possible_model_dirs = [
            os.path.join(script_dir, 'models'),  # Same directory as script
            os.path.join(os.path.dirname(script_dir), 'src', 'models'),  # ../src/models
            os.path.join(os.path.dirname(script_dir), 'models'),  # ../models
        ]
        
        model_dir = None
        for possible_dir in possible_model_dirs:
            if os.path.exists(possible_dir):
                model_dir = possible_dir
                break
        
        if model_dir is None:
            # List available directories for debugging
            available_dirs = []
            for check_dir in [script_dir, os.path.dirname(script_dir)]:
                try:
                    contents = os.listdir(check_dir)
                    available_dirs.append(f"{check_dir}: {contents}")
                except Exception:
                    pass
            
            raise FileNotFoundError(f"Model directory not found. Tried: {possible_model_dirs}. Available: {available_dirs}")
        
        # Check if model directory exists
        if not os.path.exists(model_dir):
            raise FileNotFoundError(f"Model directory not found: {model_dir}")
        
        # Load the trained models
        model_path = os.path.join(model_dir, 'model.pkl')
        vectorizer_path = os.path.join(model_dir, 'vectorizer.pkl')
        
        # Check if model files exist
        if not os.path.exists(model_path):
            raise FileNotFoundError(f"Model file not found: {model_path}")
        if not os.path.exists(vectorizer_path):
            raise FileNotFoundError(f"Vectorizer file not found: {vectorizer_path}")
        
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
        import traceback
        error_result = {
            "error": True,
            "message": str(e),
            "traceback": traceback.format_exc(),
            "original_text": text if 'text' in locals() else "",
            "script_dir": script_dir if 'script_dir' in locals() else "",
            "model_dir": model_dir if 'model_dir' in locals() else ""
        }
        print(json.dumps(error_result))
        sys.exit(1)

if __name__ == "__main__":
    main()