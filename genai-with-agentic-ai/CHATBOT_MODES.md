# Chatbot Query Modes

The chatbot now supports two intelligent modes based on the type of question:

## 🗂️ List Mode (Direct Article Retrieval)

**Triggers when users ask for:**
- Latest news
- Show me articles
- What's new in [category]
- Top news about [topic]
- Recent [category] news

**Behavior:**
- Returns **top 10 articles** directly from the database
- No LLM processing (fast response)
- Includes article title, category, and excerpt
- Supports category filtering (Technology, Health, Business, Sports, Science, Entertainment)

**Examples:**
```
User: "What are the latest news?"
Response: Shows top 10 articles across all categories

User: "Show me health news"
Response: Shows top 10 health articles

User: "Latest technology articles"
Response: Shows top 10 technology articles
```

---

## 🤖 Analytical Mode (LLM-Powered Reasoning)

**Triggers when users ask:**
- Opinion questions (will, should, can)
- Why/How questions
- Comparison questions
- Future predictions
- Impact analysis
- Any analytical query

**Behavior:**
- Retrieves relevant articles (top 5)
- Uses **LLM (Flan-T5 or Llama)** to analyze and generate answer
- Provides reasoned response based on news context
- Shows top 3 related articles as references

**Examples:**
```
User: "Will AI kill human jobs?"
Response: LLM analyzes recent AI news and provides balanced perspective + article references

User: "Why is health important?"
Response: LLM generates explanation based on health news context

User: "How will quantum computing impact business?"
Response: LLM reasoning + relevant quantum computing articles
```

---

## 🎯 Category Detection

The chatbot automatically detects categories from user queries:

- **Technology**: AI, software, tech, digital, computer, app
- **Health**: medical, disease, healthcare, doctor, wellness
- **Business**: economy, finance, market, stock, company
- **Sports**: athlete, game, football, basketball, olympic
- **Science**: research, study, discovery, experiment
- **Entertainment**: movie, music, celebrity, concert, film

---

## 🔧 Configuration

### Switching LLM Models

Edit `/app/routes/chat_routes.py`, line ~17:

```python
# Fast & lightweight (default)
llm = LocalLLM(model_name="google/flan-t5-base")

# Better quality
llm = LocalLLM(model_name="google/flan-t5-large")

# Best quality (requires HuggingFace token + GPU recommended)
llm = LocalLLM(model_name="meta-llama/Llama-2-7b-chat-hf")
```

### Adjusting Article Count

In `/app/routes/chat_routes.py`:
- Line ~131: Change `search_k = 10` for list mode
- Line ~131: Change `search_k = 5` for analytical mode
- Line ~147: Change `max_articles = 10` for list mode display

---

## 📊 Query Classification Examples

| Query | Type | Category | Articles Shown |
|-------|------|----------|----------------|
| "Latest news" | List | All | 10 |
| "Health news" | List | Health | 10 |
| "Will AI replace jobs?" | Analytical | Technology | LLM + 3 refs |
| "Why health matters?" | Analytical | Health | LLM + 3 refs |
| "Show me sports articles" | List | Sports | 10 |
| "How does this impact business?" | Analytical | Business | LLM + 3 refs |

---

## 🚀 Testing

```bash
# Start the services
./scripts/start-all.sh

# Test list mode
curl -X POST http://localhost:8000/chat/message \
  -H "Content-Type: application/json" \
  -d '{"message": "What are the latest news?"}'

# Test analytical mode
curl -X POST http://localhost:8000/chat/message \
  -H "Content-Type: application/json" \
  -d '{"message": "Will AI kill human jobs?"}'

# Test category filtering
curl -X POST http://localhost:8000/chat/message \
  -H "Content-Type: application/json" \
  -d '{"message": "Show me health news"}'
```

---

## 📝 Notes

- First LLM call takes ~10-30 seconds to download model
- Subsequent calls are fast (model cached)
- LLM responses are generated based on actual news content
- Falls back to article listing if LLM fails
- Category filters are applied when detected in query
