#!/usr/bin/env python3
"""
Warmup script to ensure NLTK data is downloaded and models can be loaded
This runs during container startup to warm up the ML service
"""

import sys
import os
import json

# Add the src directory to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

try:
    # Import and run a simple prediction to warm up everything
    from predict import main
    
    # Override sys.argv for the warmup test
    original_argv = sys.argv
    sys.argv = ['warmup.py', 'This is a warmup test message']
    
    # Redirect stdout to capture result
    import io
    from contextlib import redirect_stdout
    
    output = io.StringIO()
    with redirect_stdout(output):
        main()
    
    # Restore original argv
    sys.argv = original_argv
    
    # Parse the result to ensure it's valid
    result = json.loads(output.getvalue())
    
    if 'error' in result and result['error']:
        print(f"ERROR: Warmup failed: {result['message']}")
        sys.exit(1)
    else:
        print("SUCCESS: Warmup successful - ML service is ready!")
        print(f"SUCCESS: NLTK data ready, models loaded, test prediction: {result['prediction']}")
        sys.exit(0)
        
except Exception as e:
    print(f"ERROR: Warmup failed with exception: {str(e)}")
    sys.exit(1)