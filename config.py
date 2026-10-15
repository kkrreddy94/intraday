# Configuration settings for NSE/BSE Intraday Engine
SYMBOLS = {
    "NIFTY 50": "^NSEI",
    "NIFTY BANK": "^NSEBANK",
    "BSE SENSEX": "^BSESN"
}

TIMEFRAME = "5m"  # 5-minute timeframe recommended for intraday
DATA_PERIOD = "1d"

# Trusted RSS news feeds for accurate Indian market updates
NEWS_FEEDS = [
    "https://www.moneycontrol.com/rss/marketreports.xml",
    "https://economictimes.indiatimes.com/markets/stocks/rssfeeds/2146842.cms",
    "https://www.moneycontrol.com/rss/latestnews.xml"
]
