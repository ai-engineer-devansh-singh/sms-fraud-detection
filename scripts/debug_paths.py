#!/usr/bin/env python3
"""
Debug script to check file paths and environment on Render
"""

import sys
import os
import json

def main():
    debug_info = {
        "python_version": sys.version,
        "python_executable": sys.executable,
        "current_working_directory": os.getcwd(),
        "script_location": __file__,
        "script_directory": os.path.dirname(os.path.abspath(__file__)),
        "environment_variables": {
            "FLASK_ENV": os.environ.get("FLASK_ENV", "not_set"),
            "PATH": os.environ.get("PATH", "not_set")[:200] + "..." if os.environ.get("PATH") else "not_set"
        }
    }
    
    # Check for app.py and models
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(script_dir)
    models_dir = os.path.join(project_root, "models")
    
    debug_info["project_structure"] = {
        "script_dir": script_dir,
        "project_root": project_root,
        "models_dir": models_dir,
        "models_dir_exists": os.path.exists(models_dir)
    }
    
    # Check for app.py
    app_paths = [
        os.path.join(project_root, "app.py"),
        os.path.join(script_dir, "..", "app.py")
    ]
    
    debug_info["app_py_search"] = {}
    for i, p in enumerate(app_paths):
        debug_info["app_py_search"][f"path_{i}"] = {
            "path": p,
            "exists": os.path.exists(p)
        }
    
    # Check for model files
    model_dirs = [
        os.path.join(project_root, "models"),
        os.path.join(script_dir, "..", "models")
    ]
    
    debug_info["model_dirs_search"] = {}
    for i, model_dir in enumerate(model_dirs):
        model_files = {}
        if os.path.exists(model_dir):
            try:
                files = os.listdir(model_dir)
                model_files = {
                    "files": files,
                    "model_pkl": "model.pkl" in files,
                    "vectorizer_pkl": "vectorizer.pkl" in files
                }
            except Exception as e:
                model_files = {"error": str(e)}
        
        debug_info["model_dirs_search"][f"dir_{i}"] = {
            "path": model_dir,
            "exists": os.path.exists(model_dir),
            "contents": model_files
        }
    
    # List current directory contents
    try:
        debug_info["current_dir_contents"] = os.listdir(".")
    except Exception as e:
        debug_info["current_dir_contents"] = f"Error: {str(e)}"
    
    # List project root contents if different
    if project_root != os.getcwd():
        try:
            debug_info["project_root_contents"] = os.listdir(project_root)
        except Exception as e:
            debug_info["project_root_contents"] = f"Error: {str(e)}"
    
    print(json.dumps(debug_info, indent=2))

if __name__ == "__main__":
    main()