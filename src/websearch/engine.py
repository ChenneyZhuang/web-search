"""Core search and extraction engine."""

import urllib.request
import urllib.parse
import re
from html import unescape as _unescape
import hashlib
from pathlib import Path

CACHE_DIR = Path.home() / ".cache" / "websearch"
CACHE_DIR.mkdir(parents=True, exist_ok=True)

UA = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)"


def search(query: str, limit: int = 10) -> list[dict]:
    """DuckDuckGo HTML search. Returns list of {title, url}."""
    q = urllib.parse.quote(query)
    url = f"https://html.duckduckgo.com/html/?q={q}"
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    html = urllib.request.urlopen(req, timeout=15).read().decode("utf-8", errors="replace")

    results = []
    for u, t in re.findall(
        r'class="result__a"[^>]*href="([^"]+)"[^>]*>(.*?)</a>',
        html, re.DOTALL,
    )[:limit]:
        title = _unescape(re.sub(r"<[^>]+>", "", t).strip())
        clean_url = _clean_url(u)
        results.append({"title": title, "url": clean_url})
    return results


def extract(url: str, max_chars: int = 5000) -> str:
    """Extract readable text from a web page (with cache)."""
    cache_key = hashlib.md5(url.encode()).hexdigest()[:12]
    cache_file = CACHE_DIR / f"{cache_key}.txt"

    if cache_file.exists():
        return cache_file.read_text(encoding="utf-8")

    try:
        req = urllib.request.Request(url, headers={"User-Agent": UA})
        html = urllib.request.urlopen(req, timeout=15).read().decode("utf-8", errors="replace")
    except Exception as e:
        return f"[获取失败: {e}]"

    # Extract main content area
    body = html
    for tag in ["article", "main", 'div[class*="content"]', 'div[class*="post"]', "body"]:
        m = re.search(f"<{tag}[^>]*>(.*?)</{tag.split('[',1)[0]}>", html, re.DOTALL | re.IGNORECASE)
        if m:
            body = m.group(1)
            break

    # Clean
    text = re.sub(
        r"<(script|style|nav|footer|header|aside)[^>]*>.*?</\1>",
        "", body, flags=re.DOTALL | re.IGNORECASE,
    )
    text = re.sub(r"<[^>]+>", " ", text)
    text = re.sub(r"&[a-z]+;", " ", text)
    text = re.sub(r"\s+", " ", text).strip()
    text = text[:max_chars]

    cache_file.write_text(text, encoding="utf-8")
    return text


def search_and_extract(query: str, limit: int = 5, max_per_page: int = 3000) -> list[dict]:
    """Search + extract content in one call."""
    results = search(query, limit)
    for r in results:
        r["content"] = extract(r["url"], max_per_page)
    return results


def _clean_url(raw: str) -> str:
    """Decode DuckDuckGo redirect URLs."""
    url = raw
    if "//duckduckgo.com/l/?uddg=" in url:
        url = url.split("uddg=")[1]
    for sep in ("&rut=", "&amp;rut=", "?rut="):
        if sep in url:
            url = url.split(sep)[0]
            break
    return urllib.parse.unquote(url).replace("&amp;", "&")
