#!/usr/bin/env node

/**
 * Deployment Validation Script
 * This script validates that your SMS Spam Detection app is ready for Render deployment
 */

const fs = require("fs");
const path = require("path");

console.log("🔍 SMS Spam Detection - Deployment Validation\n");

const checks = [
  {
    name: "package.json exists",
    check: () => fs.existsSync("package.json"),
    fix: "Create package.json with npm init",
  },
  {
    name: "requirements.txt exists",
    check: () => fs.existsSync("requirements.txt"),
    fix: "Create requirements.txt with Python dependencies",
  },
  {
    name: "render.yaml exists",
    check: () => fs.existsSync("render.yaml"),
    fix: "Create render.yaml for Render deployment configuration",
  },
  {
    name: "ML model files exist",
    check: () =>
      fs.existsSync("src/models/model.pkl") &&
      fs.existsSync("src/models/vectorizer.pkl"),
    fix: "Ensure model.pkl and vectorizer.pkl are in src/models/ directory",
  },
  {
    name: "predict.py exists",
    check: () => fs.existsSync("src/predict.py"),
    fix: "Ensure predict.py is in src/ directory",
  },
  {
    name: "app.js exists",
    check: () => fs.existsSync("src/app.js"),
    fix: "Ensure app.js is in src/ directory",
  },
  {
    name: "requirements.txt has flexible versions",
    check: () => {
      if (!fs.existsSync("requirements.txt")) return false;
      const content = fs.readFileSync("requirements.txt", "utf8");
      return content.includes(">=") && !content.includes("==");
    },
    fix: "Update requirements.txt to use >= instead of == for version flexibility",
  },
];

let allPassed = true;

checks.forEach((check, index) => {
  const passed = check.check();
  const status = passed ? "✅" : "❌";
  console.log(`${index + 1}. ${check.name}: ${status}`);

  if (!passed) {
    console.log(`   💡 Fix: ${check.fix}`);
    allPassed = false;
  }
});

console.log("\n" + "=".repeat(50));

if (allPassed) {
  console.log("🎉 All checks passed! Your app is ready for Render deployment.");
  console.log("\n📋 Next steps:");
  console.log(
    '1. Commit all changes: git add . && git commit -m "Ready for deployment"'
  );
  console.log("2. Push to GitHub: git push origin main");
  console.log("3. Go to render.com and create a new Web Service");
  console.log("4. Connect your GitHub repository");
  console.log("5. Render will automatically detect render.yaml and deploy");
} else {
  console.log(
    "❌ Some checks failed. Please fix the issues above before deploying."
  );
}

console.log("\n🔗 Helpful links:");
console.log("- Render Dashboard: https://dashboard.render.com");
console.log("- Deployment Guide: Check DEPLOY.md in this project");
