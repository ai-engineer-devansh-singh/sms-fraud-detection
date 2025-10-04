const { spawn } = require("child_process");
const path = require("path");

class MLService {
  constructor() {
    this.pythonScript = path.join(__dirname, "..", "predict.py");
    // Use Python3 for production (Render) or local venv for development
    this.pythonPath =
      process.env.NODE_ENV === "production"
        ? "python3"
        : "D:/ML projects/email spam/.venv/Scripts/python.exe";
  }

  predictSpam(text) {
    return new Promise((resolve, reject) => {
      // Escape text for command line
      const escapedText = text.replace(/"/g, '\\"');

      const python = spawn(this.pythonPath, [this.pythonScript, text]);

      let result = "";
      let error = "";

      python.stdout.on("data", (data) => {
        result += data.toString();
      });

      python.stderr.on("data", (data) => {
        error += data.toString();
      });

      python.on("close", (code) => {
        if (code === 0) {
          try {
            const prediction = JSON.parse(result.trim());

            // Check if there's an error in the prediction
            if (prediction.error) {
              reject(new Error(prediction.message));
            } else {
              resolve(prediction);
            }
          } catch (e) {
            console.error("JSON Parse Error:", e);
            console.error("Raw result:", result);
            reject(new Error("Invalid JSON response from Python script"));
          }
        } else {
          console.error("Python script error:", error);
          reject(new Error(`Python script failed with code ${code}: ${error}`));
        }
      });

      python.on("error", (err) => {
        reject(new Error(`Failed to start Python process: ${err.message}`));
      });
    });
  }

  // Test method to check if the service is working
  async testConnection() {
    try {
      const testResult = await this.predictSpam("This is a test message");
      return { success: true, result: testResult };
    } catch (error) {
      return { success: false, error: error.message };
    }
  }
}

module.exports = new MLService();
