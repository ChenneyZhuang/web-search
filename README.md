# web-search

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python](https://img.shields.io/badge/python-3.9%2B-blue.svg)](https://www.python.org/downloads/)
[![Zero Dependencies](https://img.shields.io/badge/dependencies-0-brightgreen.svg)](#features)
[![CI](https://github.com/ChenneyZhuang/web-search/actions/workflows/ci.yml/badge.svg)](https://github.com/ChenneyZhuang/web-search/actions/workflows/ci.yml)
[![Release](https://img.shields.io/github/v/release/ChenneyZhuang/web-search)](https://github.com/ChenneyZhuang/web-search/releases)

**Free DuckDuckGo web search + content extraction — no API key, zero dependencies, ~90 lines of Python.**

A stdlib-only package for searching the web and extracting readable text from pages. CLI, Python API, and [Hermes Agent](https://hermes-agent.nousresearch.com) skill — same install.

---

## Quick Start

### CLI

```bash
pip install git+https://github.com/ChenneyZhuang/web-search.git
websearch "Canberra weather"              # search
websearch "solar panels" 5 --extract       # search + extract
```

### Python

```python
from websearch.engine import search, extract, search_and_extract

results = search("Canberra solar installers", limit=5)
for r in results:
    print(f"{r['title']}\n  {r['url']}")

text = extract("https://en.wikipedia.org/wiki/Canberra")
print(text[:500])

rich = search_and_extract("best cafes Canberra", limit=3)
for r in rich:
    print(f"## {r['title']}\n{r['content'][:300]}")
```

---

## Features

| Feature | Details |
|:---|:---|
| **Zero Dependencies** | Python stdlib only — no `pip install` cascade |
| **No API Key** | DuckDuckGo's public HTML interface. Free forever |
| **Content Extraction** | Strips HTML to plain text. Skips scripts, styles, nav/footer/header/aside |
| **Smart Caching** | MD5 file cache in `~/.cache/websearch/`. Second extraction is instant |
| **Clean URLs** | Auto-decodes DuckDuckGo redirect links (`uddg=...`) to real URLs |
| **CLI + Python** | Same install, both interfaces |
| **Lightweight** | ~90 lines of Python — read it in 5 minutes |

---

## Installation

```bash
pip install git+https://github.com/ChenneyZhuang/web-search.git
```

Requirements: Python 3.9+, internet connection. Linux/macOS tested; Windows should work but isn't officially tested.

---

## API Reference

All functions live in `websearch.engine`.

### `search(query, limit=10) → list[dict]`

Search DuckDuckGo and return results with `title` and `url` keys.

```python
search("capital of Australia", limit=3)
# [{"title": "Canberra - Wikipedia", "url": "https://en.wikipedia.org/wiki/Canberra"}, ...]
```

Returns an empty list if no results found. Raises `URLError` on network failure (15s timeout).

### `extract(url, max_chars=5000) → str`

Fetch a URL and extract readable text. Returns plain text with HTML stripped.

```python
text = extract("https://example.com", max_chars=2000)
```

The function tries to find the main content area in this order: `<article>` → `<main>` → div with "content"/"post" class → `<body>`. Removes script, style, nav, footer, header, aside elements, then strips all remaining HTML tags.

Results are cached to `~/.cache/websearch/`. Calling `extract()` with the same URL twice is near-instant.

On failure (network error, 404, etc.), returns `[获取失败: <error message>]` instead of raising.

### `search_and_extract(query, limit=5, max_per_page=3000) → list[dict]`

Search and extract page text in one call. Returns dicts with `title`, `url`, and `content` keys.

```python
results = search_and_extract("Python asyncio tutorial", limit=3)
for r in results:
    print(r["title"])
    print(r["content"][:200])
```

Makes `1 + limit` HTTP requests. Typical pages respond in 1–3 seconds.

---

## CLI Reference

```
websearch QUERY [LIMIT] [--extract | -e]
```

| Argument | Required | Description |
|:---|:---|:---|
| `QUERY` | Yes | Search query. Quote if it contains spaces |
| `LIMIT` | No | Number of results (default: 5) |
| `--extract`, `-e` | No | Also extract and display text from each result page |

```bash
websearch "capital of Australia"
websearch "sourdough bread" 10
websearch "noise-cancelling headphones 2026" 3 --extract
```

---

## Hermes Agent Integration

Can be used as a Hermes skill for free web search when the built-in search tool is unavailable.

```bash
pip install git+https://github.com/ChenneyZhuang/web-search.git
mkdir -p ~/.hermes/skills/web-search
cp SKILL.md ~/.hermes/skills/web-search/
```

Then in Hermes: `/skill web-search`

---

## Caching

`extract()` uses a simple file-based cache (`~/.cache/websearch/{md5_prefix}.txt`). No automatic expiration — clear manually with `rm -rf ~/.cache/websearch/` when needed. Search results are never cached — `search()` always makes a fresh request.

---

## FAQ

**Do I need an API key?** No. Uses DuckDuckGo's public HTML search page (`html.duckduckgo.com`).

**Is this legal?** DuckDuckGo's robots.txt allows automated access at reasonable rates. Designed for personal/research use, not high-volume scraping.

**Can I search in other languages?** Yes. Pass queries in any language DDG supports: `search("天气 北京")`, `search("météo Paris")`.

**What if a page blocks extraction?** Returns `[获取失败: HTTP 403]` instead of crashing — your code should handle this gracefully.

**Can I use a proxy?** Set `HTTP_PROXY` / `HTTPS_PROXY` env vars — Python's `urllib` respects them.

---

## Related

- [mcp-web-search](https://github.com/ChenneyZhuang/mcp-web-search) — MCP server wrapping this library for Claude, Cursor, Codex, etc.
- [Model Context Protocol](https://modelcontextprotocol.io)

## License

MIT
