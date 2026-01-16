// const express = require("express");
// const cors = require("cors");
// const articleRoutes = require("./routes/articleRoutes");
// const chatRoutes = require("./routes/chatRoutes");
// const app = express();

// // Middleware
// app.use(cors());
// app.use(express.json());
// app.use(express.urlencoded({ extended: false }));

// // Routes
// app.use("/api", articleRoutes);
// app.use("/api/chat", chatRoutes);

// // Health check
// app.get("/", (req, res) => {
//   res.json({ status: "Backend API Running", version: "2.0.0" });
// });

// // Global error handler
// app.use((err, _req, res, _next) => {
//   res.status(500).json({ message: err.message || "Something went wrong" });
// });

// module.exports = app;
const express = require("express");
const cors = require("cors");
const articleRoutes = require("./routes/articleRoutes");
const chatRoutes = require("./routes/chatRoutes");

const app = express();

app.use(
  cors({
    origin: [
      "https://agentic-ai-news-intelligence-platform.vercel.app",
      "http://localhost:5173",
    ],
  })
);

app.use(express.json());
app.use(express.urlencoded({ extended: false }));

app.use("/api", articleRoutes);
app.use("/api/chat", chatRoutes);

app.get("/", (_req, res) => {
  res.json({ status: "Backend API Running" });
});

module.exports = app;
