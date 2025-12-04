const axios = require("axios");

const GENAI_SERVICE_URL = process.env.GENAI_SERVICE_URL || "http://localhost:8000";

exports.getAllArticles = async (req, res) => {
  try {
    const { category, limit = 20, offset = 0 } = req.query;
    console.log("🔍 Fetching articles from GenAI service:", { category, limit, offset });
    
    const response = await axios.get(`${GENAI_SERVICE_URL}/news/fetch`, {
      params: { category, limit, offset }
    });
    
    res.json(response.data);
  } catch (err) {
    console.error("Error fetching articles:", err.message);
    res.status(500).json({ message: "Failed to fetch articles", error: err.message });
  }
};

exports.getArticleById = async (req, res) => {
  try {
    console.log("Fetching article with ID:", req.params.id);
    
    // Fetch all articles and find by ID
    const response = await axios.get(`${GENAI_SERVICE_URL}/news/fetch`, {
      params: { limit: 100 }
    });
    
    const article = response.data.find(a => a.id === req.params.id || a._id === req.params.id);
    
    if (!article) {
      return res.status(404).json({ message: "Article not found" });
    }
    
    res.json(article);
  } catch (err) {
    console.error("Error fetching article:", err.message);
    res.status(500).json({ message: "Failed to fetch article", error: err.message });
  }
};

exports.getFeaturedArticle = async (req, res) => {
  try {
    const response = await axios.get(`${GENAI_SERVICE_URL}/news/featured`);
    res.json(response.data);
  } catch (err) {
    console.error("Error fetching featured article:", err.message);
    res.status(500).json({ message: "Failed to fetch featured article", error: err.message });
  }
};

exports.getTrendingArticles = async (req, res) => {
  try {
    const limit = parseInt(req.query.limit) || 3;
    const response = await axios.get(`${GENAI_SERVICE_URL}/news/trending`, {
      params: { limit }
    });
    
    res.json(response.data);
  } catch (err) {
    console.error("Error fetching trending articles:", err.message);
    res.status(500).json({ message: "Failed to fetch trending articles", error: err.message });
  }
};

exports.searchArticles = async (req, res) => {
  try {
    const query = req.query.q;
    if (!query) {
      return res.status(400).json({ message: "Search query is required" });
    }

    const response = await axios.get(`${GENAI_SERVICE_URL}/news/search`, {
      params: { q: query }
    });

    res.json(response.data);
  } catch (err) {
    console.error("Error searching articles:", err.message);
    res.status(500).json({ message: "Failed to search articles", error: err.message });
  }
};

exports.subscribeNewsletter = async (req, res) => {
  try {
    const { email } = req.body;
    if (!email || !email.includes("@")) {
      return res.status(400).json({ message: "Invalid email address" });
    }

    console.log(`📧 Subscribed: ${email}`);
    res.json({ message: "Successfully subscribed to newsletter" });
  } catch (err) {
    res.status(500).json({ message: "Failed to subscribe" });
  }
};
