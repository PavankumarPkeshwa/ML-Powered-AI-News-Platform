// require("dotenv").config();
// const app = require("./app");
// const axios = require("axios");

// const PORT = process.env.PORT || 5000;
// const GENAI_SERVICE_URL = process.env.GENAI_SERVICE_URL || "http://localhost:8000";

// // Test GenAI service connection
// axios.get(`${GENAI_SERVICE_URL}/`)
//   .then(response => {
//     console.log("✅ GenAI Service connected:", response.data.status);
//   })
//   .catch(err => {
//     console.warn("⚠️  GenAI Service not yet available. Make sure it's running on", GENAI_SERVICE_URL);
//   });

// app.listen(PORT, () => {
//   console.log(`🚀 Backend Server running at http://localhost:${PORT}`);
//   console.log(`📡 Connecting to GenAI Service at ${GENAI_SERVICE_URL}`);
// });

require("dotenv").config();
const app = require("./app");
const axios = require("axios");

const PORT = process.env.PORT || 5000;

// ✅ Use Hugging Face URL via env variable
const GENAI_SERVICE_URL =
  process.env.GENAI_SERVICE_URL || "http://localhost:8000";

// Axios client for GenAI
const genaiClient = axios.create({
  baseURL: GENAI_BASE_URL,
  timeout: 60000, // HF cold starts
});

// 🔍 Test GenAI service health (use /docs or /health)
genaiClient
  .get("/docs")
  .then(() => {
    console.log("✅ GenAI Service connected:", GENAI_BASE_URL);
  })
  .catch(() => {
    console.warn(
      "⚠️  GenAI Service not available at",
      GENAI_BASE_URL
    );
  });

app.listen(PORT, () => {
  console.log(`🚀 Backend Server running on port ${PORT}`);
  console.log(`📡 GenAI Base URL: ${GENAI_BASE_URL}`);
});
