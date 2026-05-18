"""CLI entry point."""

import sys
from websearch.engine import search, search_and_extract


def main():
    args = sys.argv[1:]
    do_extract = "--extract" in args or "-e" in args
    args = [a for a in args if not a.startswith("-")]

    if not args:
        print("web-search — free DuckDuckGo search + content extraction")
        print("Usage: websearch 'query' [limit] [--extract]")
        print("       websearch 'Canberra weather' 5 --extract")
        sys.exit(1)

    query = args[0]
    limit = int(args[1]) if len(args) > 1 else 5

    if do_extract:
        results = search_and_extract(query, limit)
        for i, r in enumerate(results, 1):
            print(f"\n{'='*60}")
            print(f"{i}. {r['title']}")
            print(f"   {r['url']}")
            print(f"{'='*60}")
            print(r.get("content", "")[:2000])
    else:
        results = search(query, limit)
        for i, r in enumerate(results, 1):
            print(f"{i}. {r['title']}")
            print(f"   {r['url']}\n")

    if not results:
        print("(no results)")


if __name__ == "__main__":
    main()
