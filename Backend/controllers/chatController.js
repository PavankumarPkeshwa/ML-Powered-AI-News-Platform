const axios = require("axios");

const GENAI_SERVICE_URL = process.env.GENAI_SERVICE_URL || "http://localhost:8000";

exports.sendMessage = async (req, res) => {
  try {
    const { message, conversation_id } = req.body;
    
    if (!message) {
      return res.status(400).json({ message: "Message is required" });
    }

    console.log("💬 Sending message to chatbot:", message);
    
    const response = await axios.post(`${GENAI_SERVICE_URL}/chat/message`, {
      message,
      conversation_id
    });
    
    res.json(response.data);
  } catch (err) {
    console.error("Error sending message:", err.message);
    res.status(500).json({ 
      message: "Failed to send message", 
      error: err.message,
      response: "I'm sorry, I'm having trouble connecting to the AI service. Please try again later."
    });
  }
};

exports.clearConversation = async (req, res) => {
  try {
    const { conversation_id } = req.params;
    
    const response = await axios.delete(`${GENAI_SERVICE_URL}/chat/conversation/${conversation_id}`);
    
    res.json(response.data);
  } catch (err) {
    console.error("Error clearing conversation:", err.message);
    res.status(500).json({ message: "Failed to clear conversation" });
  }
};

exports.getChatbotHealth = async (req, res) => {
  try {
    const response = await axios.get(`${GENAI_SERVICE_URL}/chat/health`);
    res.json(response.data);
  } catch (err) {
    console.error("Error checking chatbot health:", err.message);
    res.status(500).json({ 
      status: "unhealthy",
      message: "Cannot connect to chatbot service" 
    });
  }
};
