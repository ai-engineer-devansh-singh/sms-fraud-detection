const express = require("express");
const router = express.Router();
const mlService = require("../services/mlService");

// POST /api/predict
router.post("/predict", async (req, res) => {
  try {
    const { text } = req.body;

    // Validation
    if (!text || typeof text !== "string") {
      return res.status(400).json({
        error: "Text field is required and must be a string",
        received: typeof text,
      });
    }

    if (text.trim().length === 0) {
      return res.status(400).json({
        error: "Text cannot be empty",
      });
    }

    // Make prediction
    const prediction = await mlService.predictSpam(text.trim());

    res.json({
      success: true,
      data: prediction,
      timestamp: new Date().toISOString(),
    });
  } catch (error) {
    console.error("Prediction error:", error);
    res.status(500).json({
      success: false,
      error: "Internal server error",
      message: error.message,
    });
  }
});

// GET /api/test
router.get("/test", (req, res) => {
  res.json({
    message: "API is working!",
    endpoints: {
      predict: "POST /api/predict",
      test: "GET /api/test",
    },
    sample_request: {
      text: "Congratulations! You've won a $1000 gift card. Click here to claim now!",
    },
  });
});

module.exports = router;
