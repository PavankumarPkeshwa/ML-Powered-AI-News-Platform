const express = require("express");
const router = express.Router();
const chatController = require("../controllers/chatController");

router.post("/message", chatController.sendMessage);
router.delete("/conversation/:conversation_id", chatController.clearConversation);
router.get("/health", chatController.getChatbotHealth);

module.exports = router;
