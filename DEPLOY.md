# SMS Spam Detection - Python Flask App - Render Deployment Guide

## 🚀 Deploy to Render

### Step 1: Prepare Your Code
1. Push your code to GitHub/GitLab
2. Make sure all files are committed:
   - `render.yaml`
   - `requirements.txt`
   - `app.py`
   - All source files

### Step 2: Deploy on Render
1. Go to [render.com](https://render.com)
2. Sign up/Login with your GitHub account
3. Click "New +" → "Blueprint"
4. Connect your repository
5. Render will automatically detect `render.yaml` and deploy

### Step 3: Alternative Manual Setup
If Blueprint doesn't work, create a Web Service manually:

1. **New Web Service**
2. **Connect Repository**
3. **Settings**:
   - **Name**: `sms-spam-detection-python`
   - **Environment**: `Python`
   - **Build Command**: 
     ```bash
     pip install -r requirements.txt && python -c "import nltk; nltk.download('stopwords'); nltk.download('punkt')"
     ```
   - **Start Command**: `python app.py`

### Step 4: Environment Variables (if needed)
- `FLASK_ENV`: `production` (automatically set by Render)
- `PORT`: (automatically set by Render)

## 📁 Project Structure for Render
```
sms-detection/
├── app.py                  # Main Flask application
├── models/
│   ├── model.pkl          # Trained ML model
│   └── vectorizer.pkl     # Text vectorizer
├── templates/
│   └── index.html         # Web interface
├── requirements.txt       # Python dependencies
├── render.yaml           # Render configuration
└── README.md
```

## 🔧 Key Files Created

### `render.yaml`
- Configures build and start commands
- Sets up Python environment

### `requirements.txt`
- Lists Python dependencies for Flask and ML model

### `app.py`
- Main Flask application with ML prediction logic

## 🌐 After Deployment

1. **Your app will be available at**: `https://your-app-name.onrender.com`
2. **API endpoint**: `https://your-app-name.onrender.com/predict`
3. **Web interface**: `https://your-app-name.onrender.com`

## 🚨 Troubleshooting

### Build Fails?
- Check build logs in Render dashboard
- Ensure all dependencies are in `requirements.txt`
- Make sure model files (`model.pkl`, `vectorizer.pkl`) are committed to git

### Python Import Errors?
- NLTK data downloads during build automatically
- Verify model files exist in `models/` directory
- Check if Python dependencies are compatible

### Production Deployment Checklist ✅

Before deploying to Render, ensure:

1. **All files are committed to git:**
   ```bash
   git add .
   git commit -m "Prepare for deployment"
   git push origin main
   ```

2. **Model files are included:**
   - `models/model.pkl` ✅
   - `models/vectorizer.pkl` ✅

3. **Configuration files are correct:**
   - `render.yaml` ✅
   - `requirements.txt` ✅ 
   - `app.py` ✅

4. **Environment detection works:**
   - App automatically detects production vs development
   - Uses built-in Flask server
   - NLTK data downloads during build

### Application Architecture

```
Production (Render):
Flask App → ML Models → JSON Response

Development (Local):
Flask App → ML Models → JSON Response
```

### Local Development
```bash
python app.py
```

### Windows: Missing Python or modules

If you see errors like "ModuleNotFoundError: No module named 'nltk'", set up Python and the required packages:

PowerShell (recommended):

```powershell
# 1. Create and activate a virtual environment in the project root
python -m venv .venv
.\.venv\Scripts\Activate.ps1

# 2. Install Python requirements
pip install -r requirements.txt

# 3. Generate models (if needed)
python generate_models.py

# 4. Run the Flask app
python app.py
```

## 💡 Tips

1. **Free Tier**: Render free tier spins down after inactivity
2. **Cold Starts**: First request may be slow
3. **Logs**: Check Render dashboard for detailed logs
4. **Custom Domain**: Available on paid plans

Ready to deploy! 🎉