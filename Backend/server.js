require("dotenv").config();
const app = require("./app");
const axios = require("axios");

const PORT = process.env.PORT || 5000;
const GENAI_SERVICE_URL = process.env.GENAI_SERVICE_URL || "http://localhost:8000";

// Test GenAI service connection
axios.get(`${GENAI_SERVICE_URL}/`)
  .then(response => {
    console.log("✅ GenAI Service connected:", response.data.status);
  })
  .catch(err => {
    console.warn("⚠️  GenAI Service not yet available. Make sure it's running on", GENAI_SERVICE_URL);
  });

app.listen(PORT, () => {
  console.log(`🚀 Backend Server running at http://localhost:${PORT}`);
  console.log(`📡 Connecting to GenAI Service at ${GENAI_SERVICE_URL}`);
});
