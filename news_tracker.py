#!/usr/bin/env python3
"""
News Tracker + News Post Generator — ALL NEWS edition
Journalist: Jhamal Symister

Platform: Kubuntu / Ubuntu 24.04 LTS (any Linux with Python 3.12+)
Uses ONLY the Python standard library — no API key, no pip installs.

Tracks ALL news categories via Google News RSS, remembers what it
has already seen, and generates a ready-to-publish news post
(Markdown) grouped by category, for any NEW stories it finds.

Categories (--all): Top Stories, Canada, World, Business, Technology,
Science, Health, Sports, Entertainment, Nvidia NVDA

Usage on Kubuntu (Konsole):
    python3 news_tracker.py --all                  # all news (default per-feed limit 5)
    python3 news_tracker.py --all --limit 8
    python3 news_tracker.py --query "Nvidia NVDA"  # single topic, as before
    python3 news_tracker.py --reset                # forget seen stories
    python3 news_tracker.py --clean                # remove cache / unneeded files only
    ./run_on_kubuntu.sh                            # launcher: runs --all and opens the post

Output:
    posts/news_post_YYYY-MM-DD.md   <- the news post, by Jhamal Symister
    seen_news.json                  <- tracking state (needed — not a cache file)
"""

import argparse
import hashlib
import html
import json
import re
import shutil
import sys
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET
from datetime import datetime
from pathlib import Path

JOURNALIST = "Jhamal Symister"
BASE_DIR = Path(__file__).resolve().parent
SEEN_FILE = BASE_DIR / "seen_news.json"
POSTS_DIR = BASE_DIR / "posts"
USER_AGENT = "NewsTracker/2.0 by Jhamal Symister (Kubuntu; Python stdlib)"
LOCALE = "hl=en-CA&gl=CA&ceid=CA:en"

# name -> ("section", topic) or ("search", query) or ("top", "")
FEEDS = [
    ("Top Stories", ("top", "")),
    ("Canada", ("search", "Canada")),
    ("World", ("section", "WORLD")),
    ("Business", ("section", "BUSINESS")),
    ("Technology", ("section", "TECHNOLOGY")),
    ("Science", ("section", "SCIENCE")),
    ("Health", ("section", "HEALTH")),
    ("Sports", ("section", "SPORTS")),
    ("Entertainment", ("section", "ENTERTAINMENT")),
    ("Nvidia NVDA", ("search", "Nvidia NVDA")),
]


def story_id(title: str, link: str) -> str:
    return hashlib.sha256(f"{title}|{link}".encode("utf-8")).hexdigest()[:16]


def load_seen() -> dict:
    if SEEN_FILE.exists():
        return json.loads(SEEN_FILE.read_text(encoding="utf-8"))
    return {}


def save_seen(seen: dict) -> None:
    SEEN_FILE.write_text(json.dumps(seen, indent=2, ensure_ascii=False), encoding="utf-8")


def clean_text(text: str) -> str:
    return re.sub(r"<[^>]+>", "", html.unescape(text or "")).strip()


def feed_url(kind: str, value: str) -> str:
    if kind == "top":
        return f"https://news.google.com/rss?{LOCALE}"
    if kind == "section":
        return f"https://news.google.com/rss/headlines/section/topic/{value}?{LOCALE}"
    q = urllib.parse.quote(value)
    return f"https://news.google.com/rss/search?q={q}&{LOCALE}"


def fetch_feed(category: str, kind: str, value: str, limit: int) -> list[dict]:
    req = urllib.request.Request(feed_url(kind, value), headers={"User-Agent": USER_AGENT})
    with urllib.request.urlopen(req, timeout=30) as resp:
        root = ET.fromstring(resp.read())
    stories = []
    for item in root.findall(".//item")[:limit]:
        title = clean_text(item.findtext("title", ""))
        link = (item.findtext("link", "") or "").strip()
        if not title or not link:
            continue
        src = item.find("source")
        stories.append({
            "id": story_id(title, link),
            "category": category,
            "title": title,
            "link": link,
            "published": (item.findtext("pubDate", "") or "").strip(),
            "source": clean_text(src.text) if src is not None and src.text else "News wire",
            "summary": clean_text(item.findtext("description", "")),
        })
    return stories


def clean_cache() -> list[str]:
    """Remove cache / unneeded files in this project only. Keeps code, posts, seen_news.json."""
    removed = []
    for p in sorted(BASE_DIR.rglob("*"), reverse=True):
        if p.is_dir() and p.name == "__pycache__":
            shutil.rmtree(p); removed.append(str(p.relative_to(BASE_DIR)) + "/")
        elif p.is_file() and (p.suffix in {".pyc", ".pyo"} or p.name in {".DS_Store"} or p.name.endswith("~")):
            p.unlink(); removed.append(str(p.relative_to(BASE_DIR)))
    # duplicate posts sitting outside posts/ (unneeded copies)
    for p in BASE_DIR.glob("news_post_*.md"):
        if (POSTS_DIR / p.name).exists():
            p.unlink(); removed.append(p.name + " (duplicate of posts/" + p.name + ")")
    return removed


def build_post(grouped_new: dict, grouped_all: dict, now: datetime, all_mode: bool) -> str:
    title = "All News — Latest Headlines" if all_mode else next(iter(grouped_all), "News")
    lines = [f"# {title}", "", f"**By {JOURNALIST}**  ", f"{now.strftime('%A, %B %d, %Y')} — Toronto", ""]
    n_new = sum(len(v) for v in grouped_new.values())
    n_all = sum(len(v) for v in grouped_all.values())
    lines += [f"{n_new} new stories tracked today, {n_all} in the latest feeds.", "", "---", ""]
    display = grouped_new if n_new else grouped_all
    for category, stories in display.items():
        if not stories:
            continue
        lines += [f"## {category}", ""]
        for i, s in enumerate(stories, 1):
            lines += [f"### {i}. {s['title']}", "", f"*{s['source']} · {s['published']}*", ""]
            if s["summary"] and s["summary"] != s["title"]:
                lines += [s["summary"], ""]
            lines += [f"[Read the full story]({s['link']})", ""]
        lines += ["---", ""]
    lines += [f"*Tracked and reported by {JOURNALIST}. Stories are deduplicated automatically on every run.*", ""]
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(description=f"All-news tracker by {JOURNALIST}")
    parser.add_argument("--all", action="store_true", help="Track all news categories")
    parser.add_argument("--query", default=None, help="Single topic (default if no --all: Nvidia NVDA)")
    parser.add_argument("--limit", type=int, default=5, help="Max stories per feed")
    parser.add_argument("--reset", action="store_true", help="Clear tracking history")
    parser.add_argument("--clean", action="store_true", help="Remove cache/unneeded files, then exit if alone")
    args = parser.parse_args()

    removed = clean_cache()
    if removed:
        print("Cleaned:", ", ".join(removed))
    if args.clean and not (args.all or args.query or args.reset):
        print(f"Cleanup done. Removed {len(removed)} item(s).")
        return 0
    if args.reset:
        save_seen({}); print("Tracking history cleared.")

    feeds = FEEDS if args.all else [(args.query or "Nvidia NVDA", ("search", args.query or "Nvidia NVDA"))]
    now = datetime.now()
    seen = load_seen()
    grouped_all, grouped_new = {}, {}
    for category, (kind, value) in feeds:
        print(f"Requesting: {category} ...")
        try:
            stories = fetch_feed(category, kind, value, args.limit)
        except Exception as e:
            print(f"  skipped ({e})", file=sys.stderr); stories = []
        # dedupe across categories too: a story already shown keeps its first category
        uniq = []
        for s in stories:
            if s["id"] not in {x["id"] for v in grouped_all.values() for x in v}:
                uniq.append(s)
        grouped_all[category] = uniq
        grouped_new[category] = [s for s in uniq if s["id"] not in seen]
        for s in uniq:
            seen[s["id"]] = {"title": s["title"], "category": category,
                             "first_seen": now.isoformat(timespec="seconds")}
    save_seen(seen)

    n_all = sum(len(v) for v in grouped_all.values())
    n_new = sum(len(v) for v in grouped_new.values())
    if not n_all:
        print("No stories returned."); return 0

    POSTS_DIR.mkdir(exist_ok=True)
    suffix = "all_news" if args.all else "news_post"
    post_path = POSTS_DIR / f"{suffix}_{now.strftime('%Y-%m-%d')}.md"
    post_path.write_text(build_post(grouped_new, grouped_all, now, args.all), encoding="utf-8")
    print(f"Fetched: {n_all} | New: {n_new} | Total tracked: {len(seen)}")
    print(f"News post written: {post_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
