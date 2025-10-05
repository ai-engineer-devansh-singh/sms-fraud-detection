# SMS Spam Detection - Render Deployment Guide

## 🚀 Deploy to Render

### Step 1: Prepare Your Code
1. Push your code to GitHub/GitLab
2. Make sure all files are committed:
   - `render.yaml`
   - `requirements.txt`
   - `package.json`
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
   - **Name**: `sms-spam-detection`
   - **Environment**: `Node`
   - **Build Command**: 
     ```bash
     pip install -r requirements.txt && python -c "import nltk; nltk.download('stopwords'); nltk.download('punkt')" && npm install
     ```
   - **Start Command**: `npm start`

### Step 4: Environment Variables (if needed)
- `NODE_ENV`: `production` (automatically set by Render)
- `PORT`: (automatically set by Render)
- `PYTHON_PATH`: (optional - if you need to specify a custom Python path)

## 📁 Project Structure for Render
```
sms-detection/
├── src/
│   ├── app.js              # Main server
│   ├── predict.py          # Python ML script
│   ├── routes/
│   ├── services/
│   └── models/
├── public/                 # Frontend files
├── package.json            # Node.js dependencies
├── requirements.txt        # Python dependencies
├── render.yaml            # Render configuration
└── README.md
```

## 🔧 Key Files Created

### `render.yaml`
- Configures build and start commands
- Sets up Python + Node.js environment

### `requirements.txt`
- Lists Python dependencies for ML model

### Updated `mlService.js`
- Uses `python3` in production
- Maintains local development compatibility

## 🌐 After Deployment

1. **Your app will be available at**: `https://your-app-name.onrender.com`
2. **API endpoint**: `https://your-app-name.onrender.com/api/predict`
3. **Web interface**: `https://your-app-name.onrender.com`

## 🚨 Troubleshooting

### Build Fails?
- Check build logs in Render dashboard
- Ensure all dependencies are in `requirements.txt`
- Verify `package.json` is valid
- Make sure model files (`model.pkl`, `vectorizer.pkl`) are committed to git

### Python Import Errors?
- NLTK data downloads during build automatically
- Verify model files exist in `src/models/` directory
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
   - `src/models/model.pkl` ✅
   - `src/models/vectorizer.pkl` ✅

3. **Configuration files are correct:**
   - `render.yaml` ✅
   - `requirements.txt` ✅ 
   - `package.json` ✅

4. **Environment detection works:**
   - App automatically detects production vs development
   - Uses `python3` in production (Render provides this)
   - Uses local virtual environment in development

### Application Architecture

```
Production (Render):
Node.js App → python3 → ML Models → JSON Response

Development (Local):
Node.js App → .venv/Scripts/python.exe → ML Models → JSON Response
```

### Local Development
```bash
npm install
npm start
```

### Windows: Missing Python or modules

If you see errors like "Failed to start Python process" or "ModuleNotFoundError: No module named 'nltk'", set up Python and the required packages:

PowerShell (recommended):

```powershell
# 1. Create and activate a virtual environment in the project root
python -m venv .venv
.\.venv\Scripts\Activate.ps1

# 2. Install Python requirements
pip install -r requirements.txt

# 3. (Optional) If using the repo's venv, point Node to it
#$env:PYTHON_PATH = (Resolve-Path .\.venv\Scripts\python.exe).Path

# 4. Run Node test script
node .\scripts\test_ml_service.js
```

If you prefer a system Python, make sure `python` or `py` is on your PATH and install the requirements globally (or in your chosen venv).

Alternatively, set the `PYTHON_PATH` environment variable to a specific Python executable path before starting the Node app.

## 💡 Tips

1. **Free Tier**: Render free tier spins down after inactivity
2. **Cold Starts**: First request may be slow
3. **Logs**: Check Render dashboard for detailed logs
4. **Custom Domain**: Available on paid plans

Ready to deploy! 🎉