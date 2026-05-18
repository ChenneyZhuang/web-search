"""web-search: free DuckDuckGo search + content extraction.

Usage:
    from websearch import search, extract, search_and_extract

    results = search("Canberra weather", limit=5)
    content = extract("https://example.com")
    full = search_and_extract("AI news", limit=3)
"""

from websearch.engine import search, extract, search_and_extract

__version__ = "0.1.0"
__all__ = ["search", "extract", "search_and_extract"]
