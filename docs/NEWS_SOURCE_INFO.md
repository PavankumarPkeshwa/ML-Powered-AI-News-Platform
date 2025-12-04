# News Sources and Article Generation - FAQ

## Where do the news articles come from?

The ML-Powered AI News Platform uses **AI-generated sample articles** to demonstrate the platform's capabilities. Here's how it works:

### Current System (Sample Articles)

The system currently uses **high-quality AI-generated sample articles** across 6 categories:

1. **Technology** - AI breakthroughs, quantum computing, battery innovations
2. **Business** - Market trends, corporate investments, e-commerce innovations
3. **Science** - Space exploration, CRISPR research, ocean discoveries
4. **Health** - Cancer treatments, microbiome research, diabetes management
5. **Sports** - Championship victories, world records, sports technology
6. **Entertainment** - Streaming success, box office records, music festivals

**Key Features:**
- 18 curated articles (3 per category)
- Professionally written with realistic content
- Proper categorization and metadata
- Relevant tags and proper source attribution
- Automatic population on system startup

**Source Attribution:**
- Articles display `source: "https://news.example.com/{category}"`
- Author: "AI News Agent"
- Images: Random placeholder images from Picsum

### Future Enhancement: Real News Scraping

The platform is **designed and ready** to collect real news from actual sources:

**Configured News Sources (Ready to Enable):**

```
Technology: TechCrunch, The Verge, Ars Technica, Wired, CNET
Business: CNBC, Bloomberg, Forbes, Business Insider, Yahoo Finance
Science: Scientific American, New Scientist, Phys.org, ScienceDaily
Health: Healthline, WebMD, Medical News Today, Health.com
Sports: ESPN, CBS Sports, Sports Illustrated, Bleacher Report
Entertainment: Variety, Hollywood Reporter, Deadline, E! Online
```

**How to Enable Real Scraping:**

The system has built-in scraping capabilities in:
- `GenAI-with-Agentic-AI/app/scraper/scraper.py` - Web scraping logic
- `GenAI-with-Agentic-AI/app/agent/manager_agent.py` - URL ingestion
- `GenAI-with-Agentic-AI/app/auto_collector.py` - Automatic collection

To enable real news collection:
1. Configure scraping frequency in `auto_collector.py`
2. Set `use_samples=False` in initialization
3. Optionally add API keys for news APIs

## Why Use Sample Articles?

**Benefits of Sample Articles:**
1. ✅ **No External Dependencies** - Works immediately without API keys
2. ✅ **Consistent Quality** - Professional, well-written content
3. ✅ **Predictable Results** - Same content for testing/demo
4. ✅ **No Rate Limits** - No concerns about API quotas
5. ✅ **Privacy Friendly** - No tracking or external requests
6. ✅ **Faster Performance** - Instant availability

**Perfect For:**
- Development and testing
- UI/UX demonstrations
- Portfolio showcases
- Learning the platform architecture

## How the AI Chatbot Works

The chatbot uses **RAG (Retrieval Augmented Generation)** with the article content:

1. **Your Question** → System searches VectorDB for relevant articles
2. **Context Retrieval** → Most relevant article content is found
3. **AI Response** → Local LLM (Flan-T5) generates answer using article context
4. **Source Attribution** → Shows which articles were used

**Example:**
```
User: "What's new in technology?"
System: Searches Technology articles in VectorDB
AI: Generates response about AI breakthroughs, quantum computing, etc.
Shows: Links to the specific articles referenced
```

## Article Quality Standards

Each sample article includes:
- **Realistic Title** - Professional news headline
- **Excerpt** - Compelling 1-2 sentence summary
- **Full Content** - 150-250 word article with multiple paragraphs
- **Metadata** - Category, tags, author, publish date, read time
- **Images** - High-quality placeholder images
- **Source Attribution** - Clear source URL

## Viewing Article Sources

When you open an article:
1. Click on any article card
2. View the full article page
3. See the source URL at the bottom
4. Check the publish date and author
5. View related tags

## Frequently Asked Questions

**Q: Are these real news articles?**
A: No, these are AI-generated sample articles designed to demonstrate the platform's capabilities with realistic, professional content.

**Q: Can I add my own articles?**
A: Yes! Use the `/scraper/ingest` endpoint to add articles from any URL, or modify `auto_collector.py` to add custom articles.

**Q: Will you add real news sources?**
A: The platform is fully capable of real news scraping. The infrastructure is ready - just needs configuration of specific news sources and scraping frequency.

**Q: How often are articles updated?**
A: Currently, articles are generated once on startup. You can enable periodic collection by uncommenting the periodic collection code in `auto_collector.py`.

**Q: Can I change the categories?**
A: Yes! Edit `shared/schema.ts` (frontend) and `auto_collector.py` (backend) to customize categories.

**Q: Where is the news data stored?**
A: Articles are stored in **ChromaDB Vector Database** at `GenAI-with-Agentic-AI/vector_store/` with embeddings for semantic search.

## System Architecture

```
News Flow:
1. auto_collector.py → Generates articles
2. VectorDB → Stores articles with embeddings
3. Backend → Fetches from VectorDB via GenAI API
4. Frontend → Displays in beautiful UI
5. Chatbot → Answers questions using RAG
```

## Need Real News?

To switch to real news scraping:

1. **Configure Sources** in `auto_collector.py`:
   ```python
   NEWS_SOURCES = {
       "Technology": ["https://your-news-source.com/tech"],
       # Add your preferred sources
   }
   ```

2. **Enable Automatic Collection**:
   ```python
   await initialize_news_collection(use_samples=False)
   ```

3. **Set Collection Frequency**:
   ```python
   await periodic_news_collection(interval_hours=6)
   ```

4. **Optional**: Add News API integration for professional news feeds

---

**Current Status**: ✅ System running with 18 high-quality sample articles across 6 categories, fully functional chatbot, and ready-to-enable real news scraping.
