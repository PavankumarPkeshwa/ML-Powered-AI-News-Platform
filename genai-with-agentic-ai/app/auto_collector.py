"""
Automated News Collection Service
This service automatically collects news from various sources on startup
and can run periodically to keep content fresh.
"""

import asyncio
import logging
from typing import List, Dict
from app.agent.manager_agent import ingest_url

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Default news sources by category (RSS and direct article URLs work better)
NEWS_SOURCES = {
    "Technology": [
        {"url": "https://techcrunch.com/feed/", "type": "rss"},
        {"url": "https://www.theverge.com/rss/index.xml", "type": "rss"},
        {"url": "https://feeds.arstechnica.com/arstechnica/index", "type": "rss"},
    ],
    "Business": [
        {"url": "https://feeds.bbci.co.uk/news/business/rss.xml", "type": "rss"},
        {"url": "https://www.cnbc.com/id/10001147/device/rss/rss.html", "type": "rss"},
    ],
    "Science": [
        {"url": "https://www.scientificamerican.com/feed/", "type": "rss"},
        {"url": "https://phys.org/rss-feed/", "type": "rss"},
    ],
    "Health": [
        {"url": "https://feeds.bbci.co.uk/news/health/rss.xml", "type": "rss"},
        {"url": "https://www.medicalnewstoday.com/rss/news.xml", "type": "rss"},
    ],
    "Sports": [
        {"url": "https://feeds.bbci.co.uk/sport/rss.xml", "type": "rss"},
        {"url": "https://www.espn.com/espn/rss/news", "type": "rss"},
    ],
    "Entertainment": [
        {"url": "https://variety.com/feed/", "type": "rss"},
        {"url": "https://deadline.com/feed/", "type": "rss"},
    ],
}

# Simpler fallback URLs that are more likely to work
FALLBACK_ARTICLES = [
    "https://example.com/tech-news",
    "https://example.com/business-news",
    "https://example.com/science-news",
]


def create_sample_articles() -> List[Dict]:
    """
    Create sample articles to populate the database initially.
    This ensures the UI has content even if scraping fails.
    """
    from datetime import datetime
    import uuid
    
    sample_articles = []
    
    # Define category-specific articles with relevant content
    # Categories: Technology, Business, Science, Health, Sports, Entertainment
    articles_by_category = {
        "Technology": [
            {
                "title": "AI Breakthrough: New Language Model Achieves Human-Level Reasoning",
                "excerpt": "Researchers unveil groundbreaking AI system that demonstrates unprecedented reasoning capabilities, marking a significant milestone in artificial intelligence development.",
                "content": """A team of researchers has unveiled a revolutionary AI language model that demonstrates human-level reasoning capabilities across diverse domains. The breakthrough system can solve complex problems, understand nuanced contexts, and generate creative solutions with remarkable accuracy.

The new model represents years of research in neural architecture design, training methodologies, and computational efficiency. Early tests show it outperforms existing systems by significant margins in tasks requiring logical reasoning, creative problem-solving, and contextual understanding.

Industry experts suggest this development could accelerate AI adoption across healthcare, education, scientific research, and business operations. The research team emphasizes responsible deployment and ethical considerations as key priorities moving forward.

This advancement opens new possibilities for human-AI collaboration, potentially transforming how we approach complex challenges in various fields. The technology is expected to become available for research partnerships later this year.""",
                "tags": ["AI", "machine learning", "research", "innovation", "technology"]
            },
            {
                "title": "Quantum Computing Achieves Major Error Correction Milestone",
                "excerpt": "Scientists successfully demonstrate stable quantum error correction, bringing practical quantum computers closer to reality.",
                "content": """In a landmark achievement, quantum computing researchers have successfully demonstrated a stable quantum error correction system that maintains quantum coherence for extended periods. This breakthrough addresses one of the most significant obstacles to building practical quantum computers.

The new error correction technique uses a novel approach that combines topological protection with active error monitoring, resulting in error rates low enough for meaningful quantum computations. The system maintained stable quantum states for over 10 seconds, far exceeding previous records.

This development has profound implications for fields requiring massive computational power, including drug discovery, climate modeling, cryptography, and materials science. Major technology companies and research institutions are already exploring partnerships to scale this technology.

Experts predict that within the next five years, we could see the first practical quantum computers capable of solving problems beyond the reach of classical supercomputers.""",
                "tags": ["quantum computing", "physics", "innovation", "research", "technology"]
            },
            {
                "title": "Revolutionary Battery Technology Promises 1000-Mile Electric Vehicle Range",
                "excerpt": "New solid-state battery design could transform electric vehicles with unprecedented range and faster charging times.",
                "content": """Engineers have developed a solid-state battery technology that could enable electric vehicles to travel over 1000 miles on a single charge while charging to 80% capacity in just 15 minutes. The breakthrough uses advanced ceramic electrolytes and lithium-metal anodes to achieve unprecedented energy density.

The new battery design addresses key limitations of current lithium-ion technology, including safety concerns, degradation over time, and charging speed. Laboratory tests demonstrate the batteries maintain 95% capacity after 5000 charge cycles, far exceeding conventional batteries.

Automotive manufacturers are expressing strong interest in the technology, with several companies already in discussions for licensing agreements. Mass production facilities are planned for 2027, with initial deployment in premium electric vehicles.

This development could accelerate the global transition to electric transportation by eliminating range anxiety and reducing charging infrastructure demands.""",
                "tags": ["battery", "electric vehicles", "energy", "innovation", "sustainability"]
            }
        ],
        "Business": [
            {
                "title": "Global Markets Rally as Economic Growth Forecasts Exceed Expectations",
                "excerpt": "Major stock indices reach record highs following unexpectedly strong economic data and positive corporate earnings reports.",
                "content": """Global financial markets experienced significant gains today as economic growth forecasts were revised upward across major economies. The rally was driven by stronger-than-expected GDP growth, declining inflation rates, and robust corporate earnings across multiple sectors.

Leading economic indicators suggest sustained growth momentum, with manufacturing activity, consumer spending, and business investment all showing positive trends. Central banks are signaling confidence in economic stability while maintaining accommodative monetary policies.

The technology and renewable energy sectors led market gains, with investors showing strong appetite for growth-oriented investments. Financial analysts recommend balanced portfolio strategies that account for both growth opportunities and potential market volatility.

Corporate executives express optimism about business conditions for the remainder of the year, citing improved supply chain efficiency, innovation investments, and expanding global markets.""",
                "tags": ["markets", "economy", "finance", "investment", "business"]
            },
            {
                "title": "Major Tech Company Announces $50 Billion Clean Energy Investment",
                "excerpt": "Industry leader commits to massive renewable energy expansion, setting new standard for corporate climate action.",
                "content": """A leading technology corporation announced a groundbreaking $50 billion investment in renewable energy infrastructure over the next decade, representing one of the largest corporate climate commitments in history. The initiative will fund solar farms, wind installations, energy storage systems, and grid modernization projects.

The company plans to achieve 100% renewable energy for all global operations by 2030 while helping transition its entire supply chain to clean energy. The investment will create thousands of jobs in renewable energy sectors and accelerate clean technology development.

Industry analysts view this announcement as a potential catalyst for broader corporate climate action, with other major companies expected to announce similar commitments. The move demonstrates how environmental responsibility and business success can align through strategic investment.

Environmental advocates praise the commitment while emphasizing the need for industry-wide transformation to address climate challenges effectively.""",
                "tags": ["renewable energy", "sustainability", "corporate", "investment", "climate"]
            },
            {
                "title": "E-Commerce Innovation Transforms Retail Shopping Experience",
                "excerpt": "New AI-powered platforms revolutionize online shopping with personalized experiences and instant delivery capabilities.",
                "content": """The retail industry is undergoing a dramatic transformation as advanced e-commerce platforms integrate artificial intelligence, augmented reality, and logistics innovations to create seamless shopping experiences. These technologies enable personalized product recommendations, virtual try-ons, and same-day delivery across major markets.

Leading retailers report significant increases in customer satisfaction and sales conversion rates following platform upgrades. The new systems use machine learning to understand individual preferences, predict needs, and optimize inventory placement for rapid fulfillment.

Small and medium businesses are also benefiting from these innovations through accessible platform services that level the competitive playing field. Industry experts predict continued rapid evolution in retail technology, with immersive shopping experiences and sustainable delivery solutions driving future growth.

Consumer behavior studies indicate strong preference for retailers that offer convenience, personalization, and environmental responsibility in their operations.""",
                "tags": ["e-commerce", "retail", "AI", "innovation", "consumer"]
            }
        ],
        "Science": [
            {
                "title": "Scientists Discover Potential Life-Supporting Exoplanet Just 40 Light-Years Away",
                "excerpt": "Astronomers identify Earth-sized planet in habitable zone with atmospheric conditions potentially suitable for life.",
                "content": """An international team of astronomers has discovered an Earth-sized exoplanet orbiting within the habitable zone of a nearby star system, just 40 light-years from our solar system. Spectroscopic analysis reveals atmospheric signatures consistent with water vapor, oxygen, and other molecules associated with biological processes.

The planet, designated Kepler-452c, orbits a sun-like star at a distance that could support liquid water on its surface. Advanced telescope observations detect seasonal variations and weather patterns similar to Earth, suggesting a dynamic climate system.

This discovery represents one of the most promising candidates for extraterrestrial life ever identified. Space agencies are prioritizing detailed observations using next-generation telescopes to characterize the planet's atmosphere and search for biosignatures.

The finding reignites discussions about humanity's place in the universe and accelerates plans for interstellar exploration missions.""",
                "tags": ["space", "astronomy", "exoplanets", "astrobiology", "discovery"]
            },
            {
                "title": "CRISPR Gene Therapy Successfully Cures Inherited Blood Disorder",
                "excerpt": "Groundbreaking clinical trial demonstrates gene editing can permanently cure genetic disease with single treatment.",
                "content": """Medical researchers report remarkable success in using CRISPR gene editing to cure patients with sickle cell disease, a debilitating inherited blood disorder affecting millions worldwide. The treatment involves editing patients' own stem cells to correct the genetic mutation causing the disease.

Clinical trial participants remain disease-free more than three years after receiving the single treatment, with no adverse effects observed. The edited cells successfully produce healthy hemoglobin, eliminating the painful symptoms and complications associated with sickle cell disease.

This breakthrough demonstrates the therapeutic potential of gene editing for treating genetic disorders. Regulatory agencies are expediting approval processes as researchers expand trials to include other inherited conditions.

Medical ethicists emphasize the importance of equitable access to these revolutionary therapies while celebrating the scientific achievement that could transform countless lives.""",
                "tags": ["genetics", "CRISPR", "medicine", "biotechnology", "healthcare"]
            },
            {
                "title": "Ocean Exploration Reveals Vast Underwater Ecosystem Teeming with Unknown Species",
                "excerpt": "Deep-sea expedition discovers thriving biological community in unexplored ocean trench, challenging understanding of life's limits.",
                "content": """A deep-sea exploration mission has uncovered a remarkable underwater ecosystem in one of Earth's deepest ocean trenches, revealing hundreds of previously unknown species thriving in extreme conditions. The discovery includes bizarre creatures adapted to crushing pressures, near-freezing temperatures, and complete darkness.

Marine biologists are studying unique adaptations these organisms employ to survive, including bioluminescence, specialized metabolisms, and symbiotic relationships. The findings provide insights into life's resilience and expand our understanding of where life can exist.

The expedition utilized advanced submersible technology and remote sensing equipment to map and sample the trench environment. Researchers discovered hydrothermal vents supporting complex food webs independent of sunlight, relying instead on chemical energy from Earth's interior.

This research has implications for astrobiology, suggesting similar life forms could exist in extreme environments on other planets and moons with subsurface oceans.""",
                "tags": ["ocean", "marine biology", "exploration", "biodiversity", "discovery"]
            }
        ],
        "Health": [
            {
                "title": "New Immunotherapy Treatment Shows 90% Success Rate Against Aggressive Cancer",
                "excerpt": "Revolutionary CAR-T cell therapy demonstrates unprecedented effectiveness in treating previously incurable cancers.",
                "content": """Oncologists announce remarkable results from clinical trials of an advanced immunotherapy treatment that achieved a 90% success rate in patients with aggressive, treatment-resistant cancers. The therapy engineers patients' immune cells to specifically target and destroy cancer cells while sparing healthy tissue.

The treatment, known as next-generation CAR-T therapy, builds upon earlier immunotherapy approaches with enhanced targeting precision and reduced side effects. Patients who exhausted conventional treatment options experienced complete remission within months of receiving the therapy.

Medical centers worldwide are preparing to offer the treatment, pending regulatory approval. The breakthrough represents years of research in immunology, genetic engineering, and personalized medicine coming together to create a potentially curative therapy.

Cancer specialists emphasize that while challenges remain, including high treatment costs and manufacturing complexity, this advancement marks a turning point in cancer treatment and offers hope to millions of patients globally.""",
                "tags": ["cancer", "immunotherapy", "medical research", "treatment", "healthcare"]
            },
            {
                "title": "Groundbreaking Study Links Gut Microbiome to Mental Health and Mood Regulation",
                "excerpt": "Research reveals powerful connection between intestinal bacteria and brain function, opening new treatment possibilities for mental health disorders.",
                "content": """A comprehensive study involving thousands of participants has established clear links between gut microbiome composition and mental health conditions including depression, anxiety, and mood disorders. The research identifies specific bacterial strains that influence neurotransmitter production and brain signaling.

Scientists discovered that microbiome diversity and balance significantly affect mental wellbeing, with certain beneficial bacteria producing compounds that regulate mood, stress responses, and cognitive function. The findings explain why diet and lifestyle factors can profoundly impact mental health.

Clinical trials are underway testing probiotic treatments and dietary interventions targeting microbiome health as complementary therapies for mental health conditions. Early results show promising improvements in symptoms and quality of life.

This research paradigm shift could transform mental health treatment by addressing underlying biological factors through accessible, non-pharmaceutical interventions alongside traditional therapies.""",
                "tags": ["mental health", "microbiome", "nutrition", "neuroscience", "wellness"]
            },
            {
                "title": "Artificial Pancreas System Revolutionizes Diabetes Management",
                "excerpt": "Automated insulin delivery system dramatically improves glucose control and quality of life for people with type 1 diabetes.",
                "content": """A fully automated artificial pancreas system has been approved for widespread use, offering people with type 1 diabetes unprecedented glucose control without constant manual monitoring and insulin adjustments. The closed-loop system uses continuous glucose monitoring and AI algorithms to automatically deliver precise insulin doses.

Clinical studies demonstrate the system maintains optimal glucose levels over 95% of the time, dramatically reducing dangerous high and low blood sugar events. Users report significant improvements in quality of life, freedom from constant diabetes management tasks, and better overall health outcomes.

The technology represents the culmination of decades of research in medical devices, sensor technology, and control algorithms. Healthcare providers are rapidly adopting the system as standard care for type 1 diabetes, with insurance coverage expanding.

Developers are working on next-generation systems for type 2 diabetes and other hormonal conditions, potentially transforming management of chronic metabolic disorders.""",
                "tags": ["diabetes", "medical devices", "healthcare technology", "chronic disease", "innovation"]
            }
        ],
        "Sports": [
            {
                "title": "Underdog Team Captures Championship in Historic Playoff Victory",
                "excerpt": "Against all odds, lower-seeded team defeats dynasty franchise to win first championship in franchise history.",
                "content": """In one of sports' greatest underdog stories, a team that barely made the playoffs staged a remarkable championship run, defeating the heavily favored defending champions in a thrilling final series. The victory marks the franchise's first championship in its 50-year history.

The team's success was driven by exceptional coaching, stellar performances from young players exceeding expectations, and an unshakeable team chemistry that overcame talent disparities. Fans celebrated throughout the night as decades of heartbreak culminated in ultimate triumph.

Sports analysts are hailing this championship as proof that determination, preparation, and teamwork can overcome superior individual talent and resources. The victory has inspired fans and athletes worldwide with its demonstration of perseverance and belief.

The championship team's journey from playoff longshot to champions will be remembered as one of sports' most inspiring achievements.""",
                "tags": ["championship", "playoffs", "underdog", "victory", "team sports"]
            },
            {
                "title": "Olympic Athlete Breaks 30-Year-Old World Record in Stunning Performance",
                "excerpt": "Remarkable athletic achievement shatters longstanding record previously thought unbreakable.",
                "content": """In a breathtaking display of human athletic potential, an Olympic competitor shattered a world record that had stood for three decades, previously considered one of sports' unbreakable barriers. The performance combined perfect technique, exceptional physical conditioning, and mental fortitude.

The record-breaking achievement came at a major international competition, with the athlete exceeding the previous mark by a significant margin that surprised even expert analysts. The performance culminated years of dedicated training, innovative coaching methods, and scientific approach to athletic preparation.

Sports scientists are studying the athlete's training regimen and biomechanics to understand how such a dramatic improvement was possible. The breakthrough may influence training approaches across multiple sports disciplines.

The athlete has become an instant global icon, inspiring a new generation to push boundaries and redefine what's possible in human athletic achievement.""",
                "tags": ["world record", "Olympics", "athletics", "performance", "achievement"]
            },
            {
                "title": "Revolutionary Sports Technology Enhances Performance While Preventing Injuries",
                "excerpt": "Advanced wearable sensors and AI analytics help athletes optimize training and reduce injury risk.",
                "content": """Professional sports teams are adopting cutting-edge wearable technology and artificial intelligence systems that monitor athlete biomechanics, physiology, and performance metrics in real-time. The systems identify injury risks, optimize training loads, and enhance performance through data-driven insights.

The technology uses advanced sensors tracking muscle activation, joint stress, metabolic markers, and movement patterns during training and competition. AI algorithms analyze this data to provide personalized recommendations for training adjustments, recovery protocols, and injury prevention strategies.

Teams implementing these systems report significant reductions in injuries, improved performance consistency, and extended athlete careers. The technology is becoming standard in professional sports and increasingly accessible to amateur athletes and fitness enthusiasts.

Sports medicine experts believe these innovations will transform athletic training, making sports safer while helping athletes reach their full potential through scientific, individualized approaches.""",
                "tags": ["sports technology", "wearables", "injury prevention", "performance", "AI"]
            }
        ],
        "Entertainment": [
            {
                "title": "Streaming Platform Announces Record-Breaking Original Series Launch",
                "excerpt": "New show becomes most-watched premiere in streaming history, drawing millions of viewers worldwide within first 24 hours.",
                "content": """A major streaming platform's latest original series has shattered viewership records, attracting over 100 million viewers globally within 24 hours of release. The show combines compelling storytelling, exceptional production value, and a talented international cast to create a cultural phenomenon.

The series success demonstrates evolving entertainment consumption patterns, with streaming platforms increasingly producing content that rivals traditional studio productions in quality and scale. Social media buzz and critical acclaim have driven unprecedented audience engagement.

Industry analysts note this achievement represents a milestone in streaming platform evolution, validating massive content investment strategies and demonstrating the platform's global reach. The success is expected to influence content production decisions across the entertainment industry.

The show's creators credit authentic storytelling, diverse representation, and commitment to quality for resonating with worldwide audiences across cultural boundaries.""",
                "tags": ["streaming", "television", "entertainment", "original content", "viewership"]
            },
            {
                "title": "Blockbuster Film Breaks Box Office Records with Global Opening Weekend",
                "excerpt": "Highly anticipated movie delivers spectacular opening, earning over $500 million worldwide in first three days.",
                "content": """The latest installment in a beloved film franchise has achieved extraordinary box office success, earning over $500 million globally during its opening weekend and setting new records across multiple markets. The film's combination of spectacular visual effects, emotional storytelling, and fan-favorite characters drew audiences to theaters in unprecedented numbers.

The success marks a significant moment for theatrical exhibition, demonstrating that compelling cinematic experiences can still drive audiences to theaters despite streaming competition. Theater chains report sold-out shows and enthusiastic audience reactions across demographics.

Film industry executives view this achievement as validation of theatrical release strategies for major productions and evidence of moviegoing's enduring appeal. The success is expected to influence production decisions and release strategies throughout the industry.

Critics praise the film for delivering on high expectations while pushing creative and technical boundaries, creating an experience that showcases cinema's unique power to entertain and inspire.""",
                "tags": ["movies", "box office", "cinema", "entertainment", "franchise"]
            },
            {
                "title": "Music Festival Returns with Unprecedented Lineup and Sustainable Practices",
                "excerpt": "Iconic event celebrates comeback with star-studded performances and commitment to environmental responsibility.",
                "content": """A legendary music festival is making its highly anticipated return with an extraordinary lineup featuring dozens of top artists across multiple genres and stages. The event also pioneers sustainable festival practices, including renewable energy, zero-waste operations, and carbon offset programs.

Organizers have invested heavily in environmental initiatives while maintaining the festival's reputation for exceptional musical experiences. Innovations include solar-powered stages, composting systems, reusable container programs, and partnerships with environmental organizations.

Music fans are excited about the diverse lineup spanning established superstars and emerging artists, with the festival providing platform for discovery alongside legendary performances. The multi-day event is expected to attract hundreds of thousands of attendees from around the world.

Industry observers note this festival's approach could establish new standards for large-scale event sustainability while demonstrating that environmental responsibility and world-class entertainment can successfully coexist.""",
                "tags": ["music festival", "live music", "sustainability", "entertainment", "concerts"]
            }
        ]
    }
    
    featured_count = 0
    
    for category, articles in articles_by_category.items():
        for article_data in articles:
            article_id = str(uuid.uuid4())
            
            article = {
                "id": article_id,
                "_id": article_id,
                "title": article_data["title"],
                "content": article_data["content"],
                "excerpt": article_data["excerpt"],
                "imageUrl": f"https://picsum.photos/seed/{article_id}/800/600",
                "author": "AI News Agent",
                "publishDate": datetime.now().isoformat(),
                "readTime": len(article_data["content"].split()) // 200 + 1,
                "category": category,
                "tags": article_data["tags"],
                "source": f"https://news.example.com/{category.lower()}",
                "isFeatured": 1 if featured_count < 3 else 0,
                "isTrending": 1 if featured_count < 6 else 0,
            }
            sample_articles.append(article)
            featured_count += 1
    
    return sample_articles


async def collect_from_source(source: dict, category: str, max_articles: int = 5) -> int:
    """
    Collect news from a single source (RSS or homepage discovery).
    Returns the number of successfully collected articles.
    """
    from app.agent.news_agent import parse_rss_feed, discover_article_links
    
    url = source.get("url")
    source_type = source.get("type", "discover")
    
    try:
        logger.info(f"📰 Processing {source_type.upper()} source: {url} ({category})")
        
        # Get article URLs based on source type
        article_urls = []
        if source_type == "rss":
            article_urls = await asyncio.to_thread(parse_rss_feed, url, max_articles)
        else:  # discover
            article_urls = await asyncio.to_thread(discover_article_links, url, max_articles)
        
        if not article_urls:
            logger.warning(f"⚠️  No articles found from {url}")
            return 0
        
        # Collect from each article URL
        successful = 0
        for article_url in article_urls:
            try:
                result = await asyncio.to_thread(ingest_url, article_url, category)
                
                if result.get("status") == "ingested":
                    successful += 1
                    logger.info(f"✅ Article collected: {article_url[:80]}...")
                    
                    # Don't overwhelm the system
                    if successful >= max_articles:
                        break
                        
                await asyncio.sleep(0.5)  # Be respectful to servers
                
            except Exception as e:
                logger.warning(f"⚠️  Failed article: {str(e)[:50]}")
                continue
        
        if successful > 0:
            logger.info(f"✅ {successful} articles from {url}")
        
        return successful
        
    except Exception as e:
        logger.error(f"❌ Error processing source {url}: {str(e)}")
        return 0


async def collect_news_for_category(category: str, sources: List[dict], limit: int = 2) -> int:
    """
    Collect news for a specific category from multiple sources.
    Returns the number of successfully collected articles.
    """
    logger.info(f"🔍 Collecting {category} news...")
    total_articles = 0
    
    for source in sources[:limit]:  # Limit number of sources
        count = await collect_from_source(source, category, max_articles=3)
        total_articles += count
        await asyncio.sleep(1)  # Be respectful to source servers
    
    return total_articles


async def auto_collect_news(quick_mode: bool = False) -> Dict[str, int]:
    """
    Automatically collect news from all categories using AI agents.
    
    AI Agent Flow:
    1. Manager Agent orchestrates the process
    2. News Agent scrapes and extracts content
    3. Validator Agent checks quality
    4. Approved articles stored in VectorDB
    
    Args:
        quick_mode: If True, collect from fewer sources (1 per category)
                   If False, collect from more sources (3 per category)
    
    Returns:
        Dictionary with collection statistics per category
    """
    logger.info("🚀 Starting AI-powered news collection...")
    logger.info("🤖 Agent Pipeline: Manager → Scraper → Validator → VectorDB")
    logger.info("📡 Using RSS feeds + article discovery for better content")
    
    stats = {}
    limit = 1 if quick_mode else 2  # Number of sources per category
    
    # Collect from all categories concurrently
    tasks = []
    for category, sources in NEWS_SOURCES.items():
        task = collect_news_for_category(category, sources, limit)
        tasks.append((category, task))
    
    # Wait for all collections to complete
    for category, task in tasks:
        count = await task
        stats[category] = count
        if count > 0:
            logger.info(f"✅ {category}: {count} articles collected successfully")
        else:
            logger.warning(f"⚠️  {category}: No articles collected (sources may be blocking)")
    
    total = sum(stats.values())
    if total > 0:
        logger.info(f"🎉 AI collection complete! {total} real articles from internet")
        logger.info(f"📊 Sources processed: {sum([min(limit, len(sources)) for sources in NEWS_SOURCES.values()])} sources")
        logger.info(f"📡 Collection methods: RSS feeds + article discovery")
    else:
        logger.error("❌ No articles collected - all sources failed or were rejected")
    
    return stats


def populate_with_samples():
    """
    Populate VectorDB with sample articles as a fallback.
    This ensures the UI always has content to display.
    """
    from app.rag.vectordb import get_vector_db
    from langchain_core.documents import Document
    
    logger.info("📝 Populating with sample articles...")
    
    try:
        vectordb = get_vector_db()
        sample_articles = create_sample_articles()
        
        documents = []
        for article in sample_articles:
            # Convert tags list to string for storage
            tags_str = ",".join(article["tags"]) if isinstance(article["tags"], list) else article["tags"]
            
            doc = Document(
                page_content=article["content"],
                metadata={
                    "id": article["id"],
                    "title": article["title"],
                    "source": article["source"],
                    "category": article["category"],
                    "author": article["author"],
                    "publishDate": article["publishDate"],
                    "imageUrl": article["imageUrl"],
                    "isFeatured": article["isFeatured"],
                    "isTrending": article["isTrending"],
                    "tags": tags_str,
                    "excerpt": article["excerpt"],
                }
            )
            documents.append(doc)
        
        # Add all documents to vectordb
        try:
            vectordb.add_documents(documents)
        except Exception:
            # Fallback method
            texts = [doc.page_content for doc in documents]
            metadatas = [doc.metadata for doc in documents]
            vectordb.add_texts(texts, metadatas=metadatas)
        
        # Persist
        try:
            vectordb.persist()
        except Exception:
            pass  # Some implementations auto-persist
        
        logger.info(f"✅ Successfully added {len(documents)} sample articles!")
        return len(documents)
        
    except Exception as e:
        logger.error(f"❌ Error populating samples: {str(e)}")
        return 0


async def initialize_news_collection(use_samples: bool = False):
    """
    Initialize the news collection system with AI agents.
    This should be called on application startup.
    
    Args:
        use_samples: If True, populate with sample articles (only as fallback)
    """
    logger.info("🌟 Initializing AI-Powered News Collection System...")
    logger.info("🤖 Agents: Manager → News Scraper → Validator → VectorDB")
    
    # Try to collect REAL news from internet first
    try:
        logger.info("🌐 Collecting real news from internet...")
        stats = await auto_collect_news(quick_mode=False)  # Full collection, not quick
        total = sum(stats.values())
        
        if total > 0:
            logger.info(f"✅ Real news collection successful! {total} articles added")
            logger.info("📊 Sources: TechCrunch, Variety, BBC, Reuters, etc.")
            return
        else:
            logger.warning("⚠️ No articles collected from real sources")
            
    except Exception as e:
        import traceback
        logger.error(f"❌ Real news collection error: {str(e)}")
        logger.error(traceback.format_exc())
    
    # Fallback to samples only if real collection completely failed AND requested
    if use_samples:
        logger.info("📝 Falling back to sample articles...")
        sample_count = populate_with_samples()
        logger.info(f"✅ Initialized with {sample_count} sample articles")
    else:
        logger.warning("⚠️ No samples loaded - UI may be empty until news is collected")
        logger.info("💡 Trigger manual collection: curl http://localhost:8000/scraper/cron")


# For manual triggering
def collect_news_sync():
    """Synchronous wrapper for manual news collection"""
    asyncio.run(auto_collect_news(quick_mode=False))


# For scheduled/periodic collection
async def periodic_news_collection(interval_hours: int = 6):
    """
    Periodically collect news at specified intervals.
    
    Args:
        interval_hours: Hours between collection runs
    """
    while True:
        try:
            logger.info(f"⏰ Running periodic news collection (every {interval_hours}h)")
            await auto_collect_news(quick_mode=False)
        except Exception as e:
            logger.error(f"❌ Periodic collection failed: {str(e)}")
        
        # Wait for next collection
        await asyncio.sleep(interval_hours * 3600)
