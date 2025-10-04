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

// Serve static files (for UI)
app.use(express.static(path.join(__dirname, "../public")));

// Routes
app.use("/api", predictionRoutes);

// Serve the main page
app.get("/", (req, res) => {
  res.sendFile(path.join(__dirname, "../public/index.html"));
});

// Health check
app.get("/health", (req, res) => {
  res.json({
    status: "OK",
    message: "SMS Spam Detection API is running",
    timestamp: new Date().toISOString(),
  });
});

app.listen(PORT, () => {
  console.log(`🚀 SMS Spam Detection Server is running on port ${PORT}`);
  console.log(`📊 API Health Check: http://localhost:${PORT}/health`);
  console.log(`🌐 Web Interface: http://localhost:${PORT}`);
});

module.exports = app;
