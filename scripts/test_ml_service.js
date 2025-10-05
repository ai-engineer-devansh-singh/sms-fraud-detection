const ml = require("../src/services/mlService");

(async () => {
  const res = await ml.testConnection();
  console.log("Test result:", res);
})();
