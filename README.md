# web-search

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

**Free DuckDuckGo web search + content extraction — no API key required.**

Zero-dependency Python package. Use as a CLI tool, Python library, or Hermes Agent skill.

## Install

```bash
pip install git+https://github.com/ChenneyZhuang/web-search.git
```

Or clone and install:

```bash
git clone https://github.com/ChenneyZhuang/web-search.git
cd web-search
pip install -e .
```

## Usage

### CLI

```bash
# Search
websearch "Canberra weather"

# Search + extract page content
websearch "DeepSeek API pricing" 3 --extract
```

### Python API

```python
from websearch import search, extract, search_and_extract

# Search (returns list of {title, url})
results = search("Canberra solar installers", limit=5)

# Extract page content
text = extract("https://example.com/article")

# Search + extract
rich = search_and_extract("best cafes Canberra", limit=3)
```

### Hermes Agent Skill

Copy `SKILL.md` to `~/.hermes/skills/web-search/`:

```bash
mkdir -p ~/.hermes/skills/web-search
cp SKILL.md ~/.hermes/skills/web-search/
```

Then in Hermes: `/skill web-search`

## Features

- **Free** — DuckDuckGo HTML scraping, no API key needed
- **Content extraction** — strips HTML and extracts readable text
- **Caching** — MD5-based file cache for extracted pages
- **Clean URLs** — auto-decodes DuckDuckGo redirect links
- **Zero dependencies** — only Python stdlib

## License

MIT
