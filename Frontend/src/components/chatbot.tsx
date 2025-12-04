import { useState, useRef, useEffect } from "react";
import { Bot, Send, X, Minimize2, Maximize2, Trash2, Sparkles } from "lucide-react";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { ScrollArea } from "@/components/ui/scroll-area";
import { Card } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { useMutation } from "@tanstack/react-query";
import { api } from "@/lib/api";

interface Message {
  role: "user" | "assistant";
  content: string;
  sources?: string[];
}

export function Chatbot() {
  const [isOpen, setIsOpen] = useState(false);
  const [isMinimized, setIsMinimized] = useState(false);
  const [messages, setMessages] = useState<Message[]>([]);
  const [input, setInput] = useState("");
  const [conversationId] = useState(`conv_${Date.now()}`);
  const messagesEndRef = useRef<HTMLDivElement>(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const sendMessageMutation = useMutation({
    mutationFn: ({ message, conversation_id }: { message: string; conversation_id: string }) =>
      api.sendChatMessage(message, conversation_id),
    onSuccess: (data) => {
      setMessages((prev) => [
        ...prev,
        {
          role: "assistant",
          content: data.response,
          sources: data.sources,
        },
      ]);
    },
    onError: () => {
      setMessages((prev) => [
        ...prev,
        {
          role: "assistant",
          content: "Sorry, I encountered an error. Please try again.",
        },
      ]);
    },
  });

  const handleSend = () => {
    if (!input.trim()) return;

    setMessages((prev) => [...prev, { role: "user", content: input }]);
    sendMessageMutation.mutate({
      message: input,
      conversation_id: conversationId,
    });
    setInput("");
  };

  const handleClear = async () => {
    try {
      await api.clearChatConversation(conversationId);
      setMessages([]);
    } catch (error) {
      console.error("Failed to clear conversation:", error);
    }
  };

  const handleKeyPress = (e: React.KeyboardEvent) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      handleSend();
    }
  };

  if (!isOpen) {
    return (
      <Button
        onClick={() => setIsOpen(true)}
        size="lg"
        className="fixed bottom-6 right-6 h-16 w-16 rounded-full shadow-2xl bg-gradient-to-br from-blue-600 to-purple-600 hover:from-blue-700 hover:to-purple-700 dark:from-blue-500 dark:to-purple-500 z-50 group"
      >
        <div className="relative">
          <Bot className="h-8 w-8 text-white group-hover:scale-110 transition-transform" />
          <div className="absolute -top-1 -right-1">
            <span className="relative flex h-3 w-3">
              <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-green-400 opacity-75"></span>
              <span className="relative inline-flex rounded-full h-3 w-3 bg-green-500"></span>
            </span>
          </div>
        </div>
      </Button>
    );
  }

  return (
    <Card className={`fixed bottom-6 right-6 z-50 shadow-2xl border-2 border-blue-200 dark:border-blue-800 transition-all duration-300 ${
      isMinimized ? "h-16 w-80" : "h-[600px] w-[400px]"
    } bg-white dark:bg-gray-900`}>
      {/* Header */}
      <div className="flex items-center justify-between p-4 border-b dark:border-gray-800 bg-gradient-to-r from-blue-600 to-purple-600 dark:from-blue-700 dark:to-purple-700 text-white rounded-t-lg">
        <div className="flex items-center space-x-3">
          <div className="relative">
            <div className="w-10 h-10 rounded-full bg-white/20 backdrop-blur-sm flex items-center justify-center">
              <Bot className="h-6 w-6" />
            </div>
            <span className="absolute bottom-0 right-0 block h-3 w-3 rounded-full bg-green-400 ring-2 ring-white"></span>
          </div>
          <div className="flex flex-col">
            <span className="font-bold text-sm">AI News Assistant</span>
            <span className="text-xs opacity-90 flex items-center gap-1">
              <Sparkles className="h-3 w-3" />
              Ask me anything!
            </span>
          </div>
        </div>
        <div className="flex items-center space-x-2">
          {messages.length > 0 && (
            <Button
              variant="ghost"
              size="icon"
              onClick={handleClear}
              className="h-8 w-8 text-white hover:bg-white/20"
            >
              <Trash2 className="h-4 w-4" />
            </Button>
          )}
          <Button
            variant="ghost"
            size="icon"
            onClick={() => setIsMinimized(!isMinimized)}
            className="h-8 w-8 text-white hover:bg-white/20"
          >
            {isMinimized ? (
              <Maximize2 className="h-4 w-4" />
            ) : (
              <Minimize2 className="h-4 w-4" />
            )}
          </Button>
          <Button
            variant="ghost"
            size="icon"
            onClick={() => setIsOpen(false)}
            className="h-8 w-8 text-white hover:bg-white/20"
          >
            <X className="h-4 w-4" />
          </Button>
        </div>
      </div>

      {!isMinimized && (
        <>
          {/* Messages */}
          <ScrollArea className="h-[440px] p-4">
            {messages.length === 0 ? (
              <div className="flex flex-col items-center justify-center h-full text-center p-6">
                <div className="w-20 h-20 rounded-full bg-gradient-to-br from-blue-100 to-purple-100 dark:from-blue-900 dark:to-purple-900 flex items-center justify-center mb-4">
                  <Bot className="h-10 w-10 text-blue-600 dark:text-blue-400" />
                </div>
                <h3 className="font-bold text-lg mb-2 text-gray-900 dark:text-white">
                  Hi! I'm your AI News Assistant 👋
                </h3>
                <p className="text-sm text-gray-600 dark:text-gray-400">
                  Ask me anything about the news articles. I can help you find information, summarize stories, or answer questions!
                </p>
                <div className="mt-4 space-y-2 w-full">
                  <button
                    onClick={() => setInput("What are the latest technology news?")}
                    className="w-full text-left p-3 rounded-lg bg-gray-100 dark:bg-gray-800 hover:bg-gray-200 dark:hover:bg-gray-700 transition-colors text-sm"
                  >
                    💡 What are the latest technology news?
                  </button>
                  <button
                    onClick={() => setInput("Tell me about AI breakthroughs")}
                    className="w-full text-left p-3 rounded-lg bg-gray-100 dark:bg-gray-800 hover:bg-gray-200 dark:hover:bg-gray-700 transition-colors text-sm"
                  >
                    🚀 Tell me about AI breakthroughs
                  </button>
                  <button
                    onClick={() => setInput("What health news do you have?")}
                    className="w-full text-left p-3 rounded-lg bg-gray-100 dark:bg-gray-800 hover:bg-gray-200 dark:hover:bg-gray-700 transition-colors text-sm"
                  >
                    🏥 What health news do you have?
                  </button>
                </div>
              </div>
            ) : (
              <div className="space-y-4">
                {messages.map((message, index) => (
                  <div
                    key={index}
                    className={`flex ${
                      message.role === "user" ? "justify-end" : "justify-start"
                    }`}
                  >
                    <div
                      className={`flex items-start space-x-2 max-w-[85%] ${
                        message.role === "user" ? "flex-row-reverse space-x-reverse" : ""
                      }`}
                    >
                      <div
                        className={`flex-shrink-0 w-8 h-8 rounded-full flex items-center justify-center ${
                          message.role === "user"
                            ? "bg-blue-600 text-white"
                            : "bg-gradient-to-br from-purple-100 to-blue-100 dark:from-purple-900 dark:to-blue-900"
                        }`}
                      >
                        {message.role === "user" ? (
                          <span className="text-sm font-bold">You</span>
                        ) : (
                          <Bot className="h-5 w-5 text-blue-600 dark:text-blue-400" />
                        )}
                      </div>
                      <div>
                        <div
                          className={`p-3 rounded-2xl ${
                            message.role === "user"
                              ? "bg-blue-600 text-white"
                              : "bg-gray-100 dark:bg-gray-800 text-gray-900 dark:text-white"
                          }`}
                        >
                          <p className="text-sm whitespace-pre-wrap">{message.content}</p>
                        </div>
                        {message.sources && message.sources.length > 0 && (
                          <div className="mt-2 flex flex-wrap gap-1">
                            {message.sources.slice(0, 2).map((source, idx) => (
                              <Badge
                                key={idx}
                                variant="outline"
                                className="text-xs bg-blue-50 dark:bg-blue-950 text-blue-700 dark:text-blue-300"
                              >
                                📎 Source {idx + 1}
                              </Badge>
                            ))}
                          </div>
                        )}
                      </div>
                    </div>
                  </div>
                ))}
                {sendMessageMutation.isPending && (
                  <div className="flex justify-start">
                    <div className="flex items-start space-x-2">
                      <div className="flex-shrink-0 w-8 h-8 rounded-full bg-gradient-to-br from-purple-100 to-blue-100 dark:from-purple-900 dark:to-blue-900 flex items-center justify-center">
                        <Bot className="h-5 w-5 text-blue-600 dark:text-blue-400" />
                      </div>
                      <div className="bg-gray-100 dark:bg-gray-800 p-3 rounded-2xl">
                        <div className="flex space-x-2">
                          <div className="w-2 h-2 bg-blue-600 rounded-full animate-bounce"></div>
                          <div className="w-2 h-2 bg-blue-600 rounded-full animate-bounce" style={{ animationDelay: "0.1s" }}></div>
                          <div className="w-2 h-2 bg-blue-600 rounded-full animate-bounce" style={{ animationDelay: "0.2s" }}></div>
                        </div>
                      </div>
                    </div>
                  </div>
                )}
                <div ref={messagesEndRef} />
              </div>
            )}
          </ScrollArea>

          {/* Input */}
          <div className="p-4 border-t dark:border-gray-800 bg-gray-50 dark:bg-gray-900/50 rounded-b-lg">
            <div className="flex space-x-2">
              <Input
                value={input}
                onChange={(e) => setInput(e.target.value)}
                onKeyPress={handleKeyPress}
                placeholder="Type your message..."
                className="flex-1 bg-white dark:bg-gray-800 border-gray-300 dark:border-gray-700"
                disabled={sendMessageMutation.isPending}
              />
              <Button
                onClick={handleSend}
                disabled={!input.trim() || sendMessageMutation.isPending}
                className="bg-gradient-to-r from-blue-600 to-purple-600 hover:from-blue-700 hover:to-purple-700 text-white"
              >
                <Send className="h-4 w-4" />
              </Button>
            </div>
            <p className="text-xs text-gray-500 dark:text-gray-400 mt-2 text-center">
              Powered by AI • Press Enter to send
            </p>
          </div>
        </>
      )}
    </Card>
  );
}
