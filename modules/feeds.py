import feedparser

NEWS_FEED_URL = "http://feeds.feedburner.com/TheHackerNews"
BLOG_FEED_URL = "https://grahamcluley.com/feed/"

def get_news():
    """Fetches and parses the news feed."""
    feed = feedparser.parse(NEWS_FEED_URL)
    return feed.entries

def get_blog_posts():
    """Fetches and parses the blog feed."""
    feed = feedparser.parse(BLOG_FEED_URL)
    return feed.entries