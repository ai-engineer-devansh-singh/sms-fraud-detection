const express = require("express");
const cors = require("cors");
const bodyParser = require("body-parser");
const path = require("path");
const predictionRoutes = require("./routes/prediction");

const app = express();
const PORT = process.env.PORT || 3000;

// Middleware
app.use(cors());
app.use(bodyParser.json());
app.use(bodyParser.urlencoded({ extended: true }));

// Serve static files (for UI) - Updated path for production
const publicPath = process.env.NODE_ENV === 'production' 
  ? path.join(__dirname, "../public")
  : path.join(__dirname, "../public");

app.use(express.static(publicPath));

// Routes
app.use("/api", predictionRoutes);

// Debug route to check file structure
app.get("/debug", (req, res) => {
  const fs = require('fs');
  const publicPath = path.join(__dirname, "../public");
  
  try {
    const publicFiles = fs.readdirSync(publicPath);
    const indexExists = fs.existsSync(path.join(publicPath, "index.html"));
    
    res.json({
      publicPath: publicPath,
      publicFiles: publicFiles,
      indexExists: indexExists,
      __dirname: __dirname,
      cwd: process.cwd()
    });
  } catch (error) {
    res.json({
      error: error.message,
      publicPath: publicPath,
      __dirname: __dirname,
      cwd: process.cwd()
    });
  }
});

// Serve the main page
app.get("/", (req, res) => {
  const indexPath = path.join(publicPath, "index.html");
  console.log("Looking for index.html at:", indexPath);
  res.sendFile(indexPath);
});

// Health check
app.get("/health", (req, res) => {
  res.json({
    status: "OK",
    message: "SMS Spam Detection API is running",
    timestamp: new Date().toISOString(),
    publicPath: publicPath,
    __dirname: __dirname
  });
});

app.listen(PORT, () => {
  console.log(`🚀 SMS Spam Detection Server is running on port ${PORT}`);
  console.log(`📊 API Health Check: http://localhost:${PORT}/health`);
  console.log(`🌐 Web Interface: http://localhost:${PORT}`);
  console.log(`📁 Public path: ${publicPath}`);
});

module.exports = app;
