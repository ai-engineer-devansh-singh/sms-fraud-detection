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
- `NODE_ENV`: `production`
- `PORT`: (automatically set by Render)

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

### Python Import Errors?
- NLTK data downloads during build
- Check if model files are included in repo

### Local Development
```bash
npm install
npm start
```

## 💡 Tips

1. **Free Tier**: Render free tier spins down after inactivity
2. **Cold Starts**: First request may be slow
3. **Logs**: Check Render dashboard for detailed logs
4. **Custom Domain**: Available on paid plans

Ready to deploy! 🎉