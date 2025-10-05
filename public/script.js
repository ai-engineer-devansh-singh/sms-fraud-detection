document.addEventListener("DOMContentLoaded", function () {
  const form = document.getElementById("predictionForm");
  const textArea = document.getElementById("smsText");
  const predictBtn = document.getElementById("predictBtn");
  const btnText = document.getElementById("btnText");
  const loadingSpinner = document.getElementById("loadingSpinner");
  const resultSection = document.getElementById("resultSection");
  const errorSection = document.getElementById("errorSection");

  form.addEventListener("submit", async function (e) {
    e.preventDefault();

    const text = textArea.value.trim();
    if (!text) {
      showError("Please enter some text to analyze.");
      return;
    }

    setLoading(true);
    hideResults();

    try {
      const response = await fetch("/api/predict", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ text: text }),
      });

      const data = await response.json();

      if (response.ok && data.success) {
        showResult(data.data);
      } else {
        showError(
          data.message || data.error || "An error occurred during prediction."
        );
      }
    } catch (error) {
      console.error("Error:", error);
      showError("Failed to connect to the server. Please try again.");
    } finally {
      setLoading(false);
    }
  });

  function setLoading(isLoading) {
    predictBtn.disabled = isLoading;
    if (isLoading) {
      btnText.textContent = "Analyzing...";
      loadingSpinner.classList.remove("hidden");
    } else {
      btnText.textContent = "Analyze SMS";
      loadingSpinner.classList.add("hidden");
    }
  }

  function hideResults() {
    resultSection.classList.add("hidden");
    errorSection.classList.add("hidden");
  }

  function showResult(data) {
    // Update prediction badge
    const predictionBadge = document.getElementById("predictionBadge");
    predictionBadge.textContent = data.is_spam
      ? "🚨 SPAM"
      : "✅ HAM (Not Spam)";
    predictionBadge.className = `badge ${data.is_spam ? "spam" : "ham"}`;

    // Update confidence bars
    const hamBar = document.getElementById("hamBar");
    const spamBar = document.getElementById("spamBar");
    const hamPercentage = document.getElementById("hamPercentage");
    const spamPercentage = document.getElementById("spamPercentage");

    const hamConfidence = data.confidence.ham * 100;
    const spamConfidence = data.confidence.spam * 100;

    // Animate the bars
    setTimeout(() => {
      hamBar.style.width = `${hamConfidence}%`;
      spamBar.style.width = `${spamConfidence}%`;
    }, 100);

    hamPercentage.textContent = `${hamConfidence.toFixed(1)}%`;
    spamPercentage.textContent = `${spamConfidence.toFixed(1)}%`;

    // Update processed text
    const processedText = document.getElementById("processedText");
    processedText.textContent =
      data.transformed_text || "No processed text available";

    // Show result section
    errorSection.classList.add("hidden");
    resultSection.classList.remove("hidden");

    // Scroll to results
    resultSection.scrollIntoView({ behavior: "smooth" });
  }

  function showError(message) {
    const errorMessage = document.getElementById("errorMessage");
    errorMessage.textContent = message;

    resultSection.classList.add("hidden");
    errorSection.classList.remove("hidden");

    // Scroll to error
    errorSection.scrollIntoView({ behavior: "smooth" });
  }
});

// Function to fill example text
function fillExample(element) {
  const exampleText = element.getAttribute("data-text");
  const textArea = document.getElementById("smsText");
  textArea.value = exampleText;

  // Add visual feedback
  element.style.transform = "scale(0.95)";
  setTimeout(() => {
    element.style.transform = "scale(1)";
  }, 150);

  // Scroll to textarea
  textArea.focus();
  textArea.scrollIntoView({ behavior: "smooth" });
}

// Add some interactive features
document.addEventListener("DOMContentLoaded", function () {
  // Auto-resize textarea
  const textArea = document.getElementById("smsText");
  textArea.addEventListener("input", function () {
    this.style.height = "auto";
    this.style.height = this.scrollHeight + "px";
  });

  // Clear button functionality
  textArea.addEventListener("input", function () {
    if (this.value.length > 0 && !document.getElementById("clearBtn")) {
      const clearBtn = document.createElement("button");
      clearBtn.type = "button";
      clearBtn.id = "clearBtn";
      clearBtn.innerHTML = "✕";
      clearBtn.style.cssText = `
                position: absolute;
                right: 10px;
                top: 10px;
                background: #ff4757;
                color: white;
                border: none;
                border-radius: 50%;
                width: 30px;
                height: 30px;
                cursor: pointer;
                font-size: 14px;
                z-index: 10;
            `;

      // Make textarea container relative
      const formGroup = this.parentElement;
      formGroup.style.position = "relative";
      formGroup.appendChild(clearBtn);

      clearBtn.addEventListener("click", function () {
        textArea.value = "";
        textArea.style.height = "auto";
        this.remove();
        textArea.focus();
        // Hide results when clearing
        document.getElementById("resultSection").classList.add("hidden");
        document.getElementById("errorSection").classList.add("hidden");
      });
    }
  });
});
