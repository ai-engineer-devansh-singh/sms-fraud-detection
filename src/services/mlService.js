const { spawn } = require("child_process");
const path = require("path");

class MLService {
  constructor() {
    this.pythonScript = path.join(__dirname, "..", "predict.py");
    this.pythonPath = process.env.PYTHON_PATH || null;

    // For production (Render), python3 should be available in PATH
    this.productionCandidates = ["python3", "python"];

    // For local development - prioritize virtual environment
    this.localCandidates = [
      "D:/ML projects/email spam/sms-detection/.venv/Scripts/python.exe",
      "python",
      "python3",
      "py",
    ];
  }

  // Probe for a working python interpreter. Returns a promise that resolves to the executable name/path.
  choosePython() {
    return new Promise((resolve, reject) => {
      // If PYTHON_PATH is explicitly set, use it
      if (this.pythonPath) {
        return resolve(this.pythonPath);
      }

      // Choose candidates based on environment
      const isProduction = process.env.NODE_ENV === "production";
      const candidates = isProduction
        ? this.productionCandidates
        : this.localCandidates;

      console.log(
        `Environment: ${
          isProduction ? "production" : "development"
        }, trying Python candidates:`,
        candidates
      );

      const tryCandidate = (idx) => {
        if (idx >= candidates.length) {
          return reject(
            new Error(
              `No suitable Python interpreter found. Tried: ${candidates.join(
                ", "
              )}. Set PYTHON_PATH environment variable or install Python.`
            )
          );
        }

        const candidate = candidates[idx];
        let out = "";
        let err = "";

        let check;
        try {
          check = spawn(candidate, ["--version"]);
        } catch (e) {
          console.log(`Failed to spawn ${candidate}:`, e.message);
          return tryCandidate(idx + 1);
        }

        check.stdout.on("data", (d) => (out += d.toString()));
        check.stderr.on("data", (d) => (err += d.toString()));

        check.on("error", (error) => {
          console.log(`Error with ${candidate}:`, error.message);
          tryCandidate(idx + 1);
        });

        check.on("close", (code) => {
          const output = (out + err).trim();
          console.log(
            `${candidate} version check - Code: ${code}, Output: ${output}`
          );

          // Accept if command printed Python version info or exited successfully
          if (code === 0 || output.toLowerCase().includes("python")) {
            console.log(`Selected Python interpreter: ${candidate}`);
            return resolve(candidate);
          }
          tryCandidate(idx + 1);
        });
      };

      tryCandidate(0);
    });
  }

  predictSpam(text) {
    return new Promise((resolve, reject) => {
      // choose a python executable first
      this.choosePython()
        .then((pythonExecutable) => {
          console.log(`Using Python: ${pythonExecutable} for prediction`);
          const python = spawn(pythonExecutable, [this.pythonScript, text]);

          let result = "";
          let error = "";

          python.stdout.on("data", (data) => (result += data.toString()));
          python.stderr.on("data", (data) => (error += data.toString()));

          python.on("close", (code) => {
            if (code === 0) {
              try {
                const prediction = JSON.parse(result.trim());
                if (prediction.error) {
                  console.error(
                    "Python script returned error:",
                    prediction.message
                  );
                  return reject(new Error(prediction.message));
                }

                // Log warnings but don't treat them as errors
                if (error.trim()) {
                  console.warn("Python warnings (non-fatal):", error.trim());
                }

                console.log(
                  "Prediction successful for text:",
                  text.substring(0, 50) + "..."
                );
                return resolve(prediction);
              } catch (e) {
                console.error("JSON Parse Error:", e);
                console.error("Raw result:", result);
                return reject(
                  new Error("Invalid JSON response from Python script")
                );
              }
            }

            // Only treat as error if exit code is non-zero
            console.error("Python script error:", error);
            console.error("Python script exit code:", code);
            return reject(
              new Error(`Python script failed with code ${code}: ${error}`)
            );
          });

          python.on("error", (err) => {
            console.error("Failed to start Python process:", err);
            return reject(
              new Error(`Failed to start Python process: ${err.message}`)
            );
          });
        })
        .catch((err) => {
          console.error("Python interpreter selection failed:", err);
          return reject(
            new Error(`No Python interpreter available: ${err.message}`)
          );
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
// Check if there's an error in the prediction
