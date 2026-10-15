import feedparser
from typing import List, Dict

class ReliableNewsFetcher:
    """
    Fetches real-time financial market updates and news from verified Indian reporting agencies 
    to filter out false breakouts and volatility shocks.
    """
    def __init__(self, feed_urls: List[str]):
        self.feed_urls = feed_urls

    def fetch_latest_news(self) -> List[Dict[str, str]]:
        news_items = []
        for url in self.feed_urls:
            try:
                feed = feedparser.parse(url)
                for entry in feed.entries[:5]:  # Top 5 recent updates per feed
                    news_items.append({
                        "title": entry.get("title", "No Title"),
                        "published": entry.get("published", "Recent"),
                        "link": entry.get("link", "#"),
                        "source": feed.feed.get("title", "Financial News")
                    })
            except Exception as e:
                print(f"Error fetching RSS feed {url}: {e}")
        return news_items
