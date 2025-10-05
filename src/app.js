const express = require("express");
const cors = require("cors");
const bodyParser = require("body-parser");
const path = require("path");
const predictionRoutes = require("./routes/prediction");
const { spawn } = require("child_process");

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

// Warmup function to ensure ML service is ready
async function warmupMLService() {
  return new Promise((resolve, reject) => {
    console.log("🔥 Warming up ML service...");

    const isProduction = process.env.NODE_ENV === "production";
    const pythonCmd = isProduction
      ? "python3"
      : "D:/ML projects/email spam/sms-detection/.venv/Scripts/python.exe";
    const warmupScript = path.join(__dirname, "..", "scripts", "warmup.py");

    const warmup = spawn(pythonCmd, [warmupScript]);

    let output = "";
    let error = "";

    warmup.stdout.on("data", (data) => {
      output += data.toString();
    });

    warmup.stderr.on("data", (data) => {
      error += data.toString();
    });

    warmup.on("close", (code) => {
      if (code === 0) {
        console.log("✅ ML service warmup completed successfully");
        if (output.trim()) console.log(output.trim());
        resolve();
      } else {
        console.error("❌ ML service warmup failed");
        if (error.trim()) console.error("Error details:", error.trim());
        reject(new Error(`Warmup failed with code ${code}`));
      }
    });

    warmup.on("error", (err) => {
      console.error("❌ Failed to start warmup process:", err);
      reject(err);
    });
  });
}

app.listen(PORT, async () => {
  console.log(`🚀 SMS Spam Detection Server is running on port ${PORT}`);
  console.log(`📊 API Health Check: http://localhost:${PORT}/health`);
  console.log(`🌐 Web Interface: http://localhost:${PORT}`);

  // Run warmup in background
  try {
    await warmupMLService();
  } catch (error) {
    console.warn(
      "⚠️ Warmup failed, but server will continue running:",
      error.message
    );
  }
});

module.exports = app;
