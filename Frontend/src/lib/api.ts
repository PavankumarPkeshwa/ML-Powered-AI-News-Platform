import { apiRequest } from "./queryClient";
import type { Article, Category } from "@shared/schema";

// API Layer
export const api = {
  // ─── Article APIs ─────────────────────────────────────
  
  getArticles: async (category?: Category, limit?: number, offset?: number): Promise<Article[]> => {
    const params = new URLSearchParams();
    if (category) params.append("category", category);
    if (limit) params.append("limit", limit.toString());
    if (offset) params.append("offset", offset.toString());

    const response = await apiRequest("GET", `/api/articles?${params.toString()}`);
    return response.json();
  },

  getArticle: async (id: string): Promise<Article> => {
    const response = await apiRequest("GET", `/api/articles/${id}`);
    return response.json();
  },

  getFeaturedArticle: async (): Promise<Article> => {
    const response = await apiRequest("GET", "/api/featured");
    return response.json();
  },

  getTrendingArticles: async (limit?: number): Promise<Article[]> => {
    const params = new URLSearchParams();
    if (limit) params.append("limit", limit.toString());

    const response = await apiRequest("GET", `/api/trending?${params.toString()}`);
    return response.json();
  },

  searchArticles: async (query: string): Promise<Article[]> => {
    const params = new URLSearchParams({ q: query });
    const response = await apiRequest("GET", `/api/search?${params.toString()}`);
    return response.json();
  },

  subscribeNewsletter: async (email: string): Promise<{ message: string }> => {
    const response = await apiRequest("POST", "/api/newsletter", { email });
    return response.json();
  },

  // ─── Chatbot APIs ─────────────────────────────────────

  sendChatMessage: async (message: string, conversationId?: string): Promise<{
    response: string;
    conversation_id: string;
    sources: string[];
  }> => {
    const response = await apiRequest("POST", "/api/chat/message", { 
      message, 
      conversation_id: conversationId 
    });
    return response.json();
  },

  clearChatConversation: async (conversationId: string): Promise<{ message: string }> => {
    const response = await apiRequest("DELETE", `/api/chat/conversation/${conversationId}`);
    return response.json();
  },

  getChatbotHealth: async (): Promise<{ status: string; message: string }> => {
    const response = await apiRequest("GET", "/api/chat/health");
    return response.json();
  },

  // ─── Admin APIs ──────────────────────────────────────

  getAdminStatus: async (): Promise<{
    scheduler: {
      isRunning: boolean;
      nextRun: string;
      lastRun: string;
    };
    database: {
      totalArticles: number;
      categoryCounts: Array<{
        _id: string;
        count: number;
        avgLikes: number;
      }>;
      lastUpdated: string;
    };
    timestamp: string;
  }> => {
    const response = await apiRequest("GET", "/api/admin/status");
    return response.json();
  },

  scrapeNews: async (): Promise<{ message: string }> => {
    const response = await apiRequest("POST", "/api/admin/scrape");
    return response.json();
  },

  cleanupArticles: async (days: number): Promise<{ message: string }> => {
    const response = await apiRequest("POST", "/api/admin/cleanup", {
      days,
    });
    return response.json();
  },
};
