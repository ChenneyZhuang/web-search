# web-search

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python](https://img.shields.io/badge/python-3.9%2B-blue.svg)](https://www.python.org/downloads/)
[![Zero Dependencies](https://img.shields.io/badge/dependencies-0-brightgreen.svg)](#features)
[![Platform](https://img.shields.io/badge/platform-linux%20%7C%20macos-lightgrey.svg)](#installation)
[![CI](https://github.com/ChenneyZhuang/web-search/actions/workflows/ci.yml/badge.svg)](https://github.com/ChenneyZhuang/web-search/actions/workflows/ci.yml)

**Free DuckDuckGo web search + content extraction — no API key required.**

A zero-dependency Python package that lets you search the web and extract readable text from pages. Use it as a CLI tool, a Python library, or a [Hermes Agent](https://hermes-agent.nousresearch.com) skill.

---

## Table of Contents

- [What It Does](#what-it-does)
- [Features](#features)
- [Installation](#installation)
- [Quick Start](#quick-start)
  - [CLI](#cli-quick-start)
  - [Python API](#python-quick-start)
- [API Reference](#api-reference)
  - [`search()`](#search)
  - [`extract()`](#extract)
  - [`search_and_extract()`](#search_and_extract)
- [CLI Reference](#cli-reference)
- [Hermes Agent Integration](#hermes-agent-integration)
- [Caching Behavior](#caching-behavior)
- [FAQ](#faq)
- [License](#license)

---

## What It Does

`web-search` performs two main jobs:

1. **Web Search** — Queries DuckDuckGo's HTML search interface and returns results as clean `{title, url}` dictionaries. No API key, no account, no credit card — it just works.

2. **Content Extraction** — Fetches a URL, strips away all the HTML, JavaScript, navigation menus, and ads, then returns just the readable text. Great for feeding page content into LLMs or doing your own analysis.

You can also combine both in a single call: search for something, then automatically extract the text from every result page. One line of code, done.

---

## Features

| Feature | Details |
|:---|:---|
| **Zero Dependencies** | Uses only Python's standard library — no `pip install` cascade of 50 packages. |
| **No API Key** | Scrapes DuckDuckGo's public HTML interface. Free forever. |
| **Content Extraction** | Strips HTML to readable plain text. Skips scripts, styles, nav/footer/header/aside elements. |
| **HTML Entity Decoding** | Titles come out clean — `&#x27;` becomes `'`, `&amp;` becomes `&`, etc. |
| **Smart Caching** | MD5-based file cache in `~/.cache/websearch/`. Extract the same URL twice and the second call is instant. |
| **Clean URLs** | DuckDuckGo wraps results in redirect links (`uddg=...&rut=...`). This library decodes them back to the real destination URL automatically. |
| **CLI + Python + Hermes** | Three ways to use it, all from the same install. |
| **PEP 561 Typed** | Ships `py.typed` marker — compatible with mypy, pylance, and IDE autocompletion. |
| **Lightweight** | The entire source is ~90 lines of Python. Easy to read, audit, and hack on. |

---

## Installation

### Option 1: pip install from GitHub (recommended)

```bash
pip install git+https://github.com/ChenneyZhuang/web-search.git
```

This is the simplest method. It installs the latest version from the `main` branch.

### Option 2: Clone and install locally

```bash
git clone https://github.com/ChenneyZhuang/web-search.git
cd web-search
pip install -e .
```

The `-e` flag ("editable install") means changes you make to the source code take effect immediately — great if you plan to modify or contribute.

### Option 3: Install as a Hermes Agent skill

If you use [Hermes Agent](https://hermes-agent.nousresearch.com), you can install this as a skill:

```bash
# First install the package
pip install git+https://github.com/ChenneyZhuang/web-search.git

# Then register the skill
mkdir -p ~/.hermes/skills/web-search
cp SKILL.md ~/.hermes/skills/web-search/
```

Then in Hermes, run `/skill web-search` to activate it.

### Requirements

- **Python 3.9 or newer** (uses `urllib.request`, type hints like `list[dict]`)
- **Linux or macOS** (tested on both; Windows may work but isn't officially tested)
- **Internet connection** (obviously — it's a web search tool!)

---

## Quick Start

### CLI Quick Start

After installation, the `websearch` command is available in your terminal:

```bash
# Basic search — returns titles and URLs
websearch "Canberra weather"

# Specify how many results (default is 5)
websearch "best pizza in Brooklyn" 10

# Search AND extract the text from each page
websearch "DeepSeek API pricing" 3 --extract

# Same thing, short flag
websearch "solar panels Canberra" 5 -e
```

**Sample output** (search-only mode):

```
1. Canberra Weather Forecast - Bureau of Meteorology
   http://www.bom.gov.au/act/forecasts/canberra.shtml

2. Canberra Weather - AccuWeather
   https://www.accuweather.com/en/au/canberra/2600/weather-forecast/13285
...
```

**Sample output** (with `--extract`):

```
============================================================
1. Canberra Weather Forecast - Bureau of Meteorology
   http://www.bom.gov.au/act/forecasts/canberra.shtml
============================================================
Canberra area. Partly cloudy. Medium chance of showers, most
likely in the morning and afternoon. Light winds becoming...
```

### Python Quick Start

```python
from websearch.engine import search, extract, search_and_extract

# ── Search the web ─────────────────────────────────────
results = search("Canberra solar installers", limit=5)
for r in results:
    print(f"{r['title']}")
    print(f"  {r['url']}\n")

# ── Extract text from a single URL ─────────────────────
text = extract("https://en.wikipedia.org/wiki/Canberra")
print(text[:500])  # First 500 characters

# ── Search AND extract in one call ─────────────────────
rich_results = search_and_extract("best cafes Canberra", limit=3)
for r in rich_results:
    print(f"## {r['title']}")
    print(r['content'][:300])
    print("---")
```

---

## API Reference

All functions live in `websearch.engine`.

### `search()`

Search DuckDuckGo and return a list of results.

```python
search(query: str, limit: int = 10) -> list[dict]
```

#### Parameters

| Parameter | Type | Default | Description |
|:---|:---|:---|:---|
| `query` | `str` | *(required)* | The search query. Can be anything you'd type into DuckDuckGo — natural language, keywords, phrases in quotes, etc. |
| `limit` | `int` | `10` | Maximum number of results to return. DuckDuckGo's HTML page returns around 20–25 results; values above that will just return whatever's available. |

#### Returns

A list of dictionaries, each with two keys:

| Key | Type | Description |
|:---|:---|:---|
| `title` | `str` | The page title as displayed in DuckDuckGo's results. |
| `url` | `str` | The **cleaned, decoded** destination URL. DuckDuckGo's redirect wrapper is automatically stripped. |

#### Example return value

```python
[
    {
        "title": "Canberra - Wikipedia",
        "url": "https://en.wikipedia.org/wiki/Canberra"
    },
    {
        "title": "Visit Canberra - Official Tourism Website",
        "url": "https://visitcanberra.com.au/"
    },
    ...
]
```

#### Notes

- Results are extracted from DuckDuckGo's HTML interface (`html.duckduckgo.com`), which is their no-JavaScript version. This means results may differ slightly from the JavaScript-heavy main site.
- The function makes a single HTTP request. No pagination.
- If DuckDuckGo returns no results, you'll get an empty list `[]`.
- A `urllib.error.URLError` (or similar) is raised on network failure (timeout is 15 seconds).

---

### `extract()`

Fetch a URL and extract the readable text content.

```python
extract(url: str, max_chars: int = 5000) -> str
```

#### Parameters

| Parameter | Type | Default | Description |
|:---|:---|:---|:---|
| `url` | `str` | *(required)* | The URL of the page to extract text from. Must be a full URL including `https://`. |
| `max_chars` | `int` | `5000` | Maximum number of characters to return. Text beyond this limit is truncated. Useful for keeping LLM prompts concise. |

#### Returns

A plain-text string with the extracted content. If the page cannot be fetched (network error, 404, etc.), returns a string like `[获取失败: <error message>]`.

#### How extraction works

The function tries to find the main content area in this order of priority:

1. `<article>` tag
2. `<main>` tag
3. `<div>` with a class containing "content" or "post"
4. `<body>` tag (fallback — the whole page)

Once the content area is found, it:

- Removes `<script>`, `<style>`, `<nav>`, `<footer>`, `<header>`, and `<aside>` elements
- Strips all remaining HTML tags
- Collapses whitespace
- Truncates to `max_chars`

#### Caching

Results are cached to disk (see [Caching Behavior](#caching-behavior)). Calling `extract()` with the same URL a second time is near-instant.

#### Example

```python
text = extract("https://example.com/article", max_chars=2000)
print(text)
```

---

### `search_and_extract()`

Search the web and extract text from each result — all in one call.

```python
search_and_extract(query: str, limit: int = 5, max_per_page: int = 3000) -> list[dict]
```

#### Parameters

| Parameter | Type | Default | Description |
|:---|:---|:---|:---|
| `query` | `str` | *(required)* | The search query. Passed directly to `search()`. |
| `limit` | `int` | `5` | Maximum number of search results. Passed to `search()`. |
| `max_per_page` | `int` | `3000` | Maximum characters to extract from each result page. Passed to `extract()` as `max_chars`. |

#### Returns

A list of dictionaries, each with three keys:

| Key | Type | Description |
|:---|:---|:---|
| `title` | `str` | The page title. |
| `url` | `str` | The cleaned URL. |
| `content` | `str` | The extracted text content (up to `max_per_page` characters). |

#### Example

```python
results = search_and_extract("Python asyncio tutorial", limit=3, max_per_page=2000)
for r in results:
    print(r["title"])
    print(r["url"])
    print(r["content"][:200])
    print("---")
```

#### Performance note

This function makes `1 + limit` HTTP requests (one for the search, then one for each result). With `limit=5` and a 15-second timeout per request, worst-case total time is ~90 seconds, though typical pages respond in 1–3 seconds.

---

## CLI Reference

```
websearch QUERY [LIMIT] [--extract | -e]
```

### Arguments

| Argument | Required | Description |
|:---|:---|:---|
| `QUERY` | Yes | The search query. Wrap in quotes if it contains spaces. |
| `LIMIT` | No | Number of results (default: `5`). Must be a plain integer. |
| `--extract`, `-e` | No | If present, also extract and display text from each result page. |

### Examples

```bash
# Simple search, default 5 results
websearch "capital of Australia"

# 10 results
websearch "how to make sourdough bread" 10

# 3 results with extracted content
websearch "best noise-cancelling headphones 2026" 3 --extract

# Same, using short flag
websearch "top sci-fi books" 5 -e
```

### Exit codes

| Code | Meaning |
|:---|:---|
| `0` | Success (results found and displayed). |
| `1` | No query provided (help text shown). |

---

## Hermes Agent Integration

`web-search` was designed with Hermes Agent in mind. When the built-in web search tool is unavailable or rate-limited, this skill provides a free alternative with the added bonus of content extraction.

### Installing as a Hermes skill

1. **Install the Python package:**

   ```bash
   pip install git+https://github.com/ChenneyZhuang/web-search.git
   ```

2. **Register the skill file:**

   ```bash
   mkdir -p ~/.hermes/skills/web-search
   cp SKILL.md ~/.hermes/skills/web-search/
   ```

3. **Activate in Hermes chat:**

   ```
   /skill web-search
   ```

### Using the skill in Hermes

Once the skill is active, Hermes can call it through its `execute_code` or `terminal` tools. The skill tells Hermes to prefer this tool over the built-in search.

**Example Hermes interactions:**

> **User:** "Search for the latest news about the James Webb Space Telescope"
>
> **Hermes** (using the skill):
> ```python
> from websearch.engine import search_and_extract
> results = search_and_extract("James Webb Space Telescope latest news 2026", limit=3)
> ```
> Then summarizes the results for the user.

**Via terminal in Hermes:**

```bash
python3 -c "from websearch.engine import search; import json; print(json.dumps(search('Canberra weather', 5), indent=2))"
```

### Why use this over Hermes's built-in search?

- **Free** — no API key, no rate limits, no quota to exhaust
- **Redundant** — works even when Hermes's search backend is down
- **Content extraction** — gets the actual page text, not just snippets
- **Caching** — repeated extractions are instant

---

## Caching Behavior

`extract()` uses a simple file-based cache to avoid re-fetching the same URL repeatedly.

### How it works

1. When you call `extract(url)`, the function computes an MD5 hash of the URL and takes the first 12 hex characters as the cache key.
2. It checks `~/.cache/websearch/{key}.txt` for a cached result.
3. If the cache file exists, it returns the cached text immediately (no network request).
4. If not, it fetches the page, extracts the text, writes it to the cache file, and returns it.

### Cache location

```
~/.cache/websearch/
```

Example:

```
~/.cache/websearch/a1b2c3d4e5f6.txt
~/.cache/websearch/9f8e7d6c5b4a.txt
```

### Cache management

- **To clear the cache entirely:**
  ```bash
  rm -rf ~/.cache/websearch/
  ```
  The directory is recreated automatically on the next `extract()` call.

- **To clear a specific URL's cache:**
  ```python
  import hashlib
  key = hashlib.md5("https://example.com/page".encode()).hexdigest()[:12]
  # Then delete ~/.cache/websearch/{key}.txt
  ```

- **Cache never expires automatically.** If a page changes, you must clear the cache manually for that URL. In practice, this is rarely an issue for short-lived LLM sessions — the freshness of results is usually "good enough" for one conversation.

### Search results are NOT cached

Only `extract()` uses the cache. `search()` always makes a fresh request to DuckDuckGo, so search results are always current.

---

## FAQ

### Do I need an API key?

**No.** This library scrapes DuckDuckGo's public HTML search page (the no-JavaScript version at `html.duckduckgo.com`). No account, no key, no registration required.

### Is this legal?

DuckDuckGo's robots.txt does not disallow the HTML search endpoint, and the library makes reasonable, low-volume requests (one per query, with a 15-second timeout). For personal and research use, this is fine. If you plan to make high-volume automated queries, review DuckDuckGo's terms of service and consider using their [official Instant Answer API](https://duckduckgo.com/api) instead.

### Why are my search results different from duckduckgo.com?

This library uses DuckDuckGo's **HTML-only** interface (`html.duckduckgo.com`), which is designed for browsers without JavaScript. The results may differ slightly from the JavaScript-rich main site, but the core results are the same.

### Can I use this on Windows?

It hasn't been tested on Windows, but since it uses only standard-library modules (`urllib`, `pathlib`, `hashlib`, `re`), it **should** work. The cache directory uses `Path.home() / ".cache" / "websearch"`, which resolves correctly on Windows (`C:\Users\<name>\.cache\websearch\`). If you try it and run into issues, please open a GitHub issue.

### How do I extract more text from a page?

Increase the `max_chars` parameter:

```python
# Get up to 20,000 characters
text = extract("https://example.com/long-article", max_chars=20000)
```

Or in the CLI, you can't customize `max_chars` directly — but you can use the Python API for full control.

### What happens if a page blocks the request?

The function returns a string like `[获取失败: HTTP Error 403: Forbidden]` instead of raising an exception. This is intentional — when processing multiple pages, one failure shouldn't crash your entire operation. The content will just be the error message.

### Can I search in languages other than English?

Yes! Pass your query in any language DuckDuckGo supports:

```python
search("天气 北京", limit=5)        # Chinese
search(" météo Paris", limit=5)     # French
search("東京 天気", limit=5)         # Japanese
```

The query is URL-encoded automatically.

### How is this different from the `duckduckgo_search` pip package?

The `duckduckgo_search` package (by deedy5) is a more feature-rich alternative with support for images, videos, news, and instant answers. `web-search` is intentionally minimal: zero dependencies, ~85 lines of code, and focused on just text search + content extraction. Choose based on your needs.

### Why does `search_and_extract` take so long?

Each result page is fetched sequentially (not in parallel) with a 15-second timeout. With `limit=5`, that's up to 5 extra HTTP requests. If speed matters, use `search()` to get the URLs first, then selectively `extract()` only the pages you care about.

---

## License

MIT — see the [LICENSE](LICENSE) file for the full text.

Built with ❤️ by [Chenney Zhuang](https://github.com/ChenneyZhuang).
