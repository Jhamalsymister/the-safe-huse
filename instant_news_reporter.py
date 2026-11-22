#!/usr/bin/env python3
"""
Instant News Reporter — by Journalist Jhamal Symister
Platform: Kubuntu / Ubuntu 24.04, Python 3.12+, standard library ONLY.

Fetches ALL news categories IN PARALLEL (instant), builds an instant
report, and prepares a ready-to-send submission for EVERY news site
that accepts journalist / public news reports — plus Jay's own
connected social sites (Instagram, Facebook, Threads).
YouTube is intentionally NOT included (Jay cancelled it Nov. 21, 2026).

Usage:
    python3 instant_news_reporter.py                 # instant report + outbox pack
    python3 instant_news_reporter.py --limit 5
    python3 instant_news_reporter.py --send          # also email the tip sites
        --send needs mail config in environment (never hard-code a password):
        NEWS_SMTP_HOST, NEWS_SMTP_PORT (default 587), NEWS_SMTP_USER,
        NEWS_SMTP_PASS, NEWS_FROM  (e.g. your Gmail with an app password)
        Without config, --send safely falls back to drafts and tells you.

Output:
    posts/instant_report_YYYY-MM-DD_HHMM.md
    outbox/<site>_submission.txt   (To / Subject / Body, ready to send)
    outbox/social_post.txt         (Instagram / Facebook / Threads)
    outbox/INDEX.md                (checklist of every site + status)
"""

import argparse
import hashlib
import html
import json
import os
import re
import shutil
import smtplib
import sys
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime
from email.message import EmailMessage
from pathlib import Path

sys.dont_write_bytecode = True  # keep the folder cache-free
JOURNALIST = "Jhamal Symister"
BASE_DIR = Path(__file__).resolve().parent
SEEN_FILE = BASE_DIR / "seen_news.json"
POSTS_DIR = BASE_DIR / "posts"
OUTBOX_DIR = BASE_DIR / "outbox"
LOCALE = "hl=en-CA&gl=CA&ceid=CA:en"
UA = "InstantNewsReporter/1.0 by Jhamal Symister (Kubuntu; Python stdlib)"

FEEDS = [
    ("Top Stories", ("top", "")), ("Canada", ("search", "Canada")),
    ("World", ("section", "WORLD")), ("Business", ("section", "BUSINESS")),
    ("Technology", ("section", "TECHNOLOGY")), ("Science", ("section", "SCIENCE")),
    ("Health", ("section", "HEALTH")), ("Sports", ("section", "SPORTS")),
    ("Entertainment", ("section", "ENTERTAINMENT")), ("Nvidia NVDA", ("search", "Nvidia NVDA")),
]

# News sites that accept journalist / public reports (tip addresses checked Nov. 21, 2026)
TIP_SITES = [
    ("CP24", "email", "breakingnews@cp24.com"),
    ("CTV News", "email", "news@ctv.ca"),
    ("Global News", "email", "newstips@globaltv.com"),
    ("The Canadian Press", "email", "editorial@thecanadianpress.com"),
    ("The Globe and Mail", "email", "Newsroom@globeandmail.com"),
    ("CityNews", "web form", "CityNews submit page (citynews.ca)"),
    ("CBC News Toronto", "web form", "CBC News 'send a news tip' page (cbc.ca)"),
]
SOCIAL_SITES = ["Instagram @jhamalericsymister", "Facebook", "Threads"]


def clean_cache() -> None:
    for p in sorted(BASE_DIR.rglob("*"), reverse=True):
        if p.is_dir() and p.name == "__pycache__":
            shutil.rmtree(p)
        elif p.is_file() and p.suffix in {".pyc", ".pyo"}:
            p.unlink()


def sid(title, link):
    return hashlib.sha256(f"{title}|{link}".encode()).hexdigest()[:16]


def txt(t):
    return re.sub(r"<[^>]+>", "", html.unescape(t or "")).strip()


def feed_url(kind, value):
    if kind == "top":
        return f"https://news.google.com/rss?{LOCALE}"
    if kind == "section":
        return f"https://news.google.com/rss/headlines/section/topic/{value}?{LOCALE}"
    return f"https://news.google.com/rss/search?q={urllib.parse.quote(value)}&{LOCALE}"


def fetch(args):
    category, (kind, value), limit = args
    req = urllib.request.Request(feed_url(kind, value), headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=30) as r:
        root = ET.fromstring(r.read())
    out = []
    for item in root.findall(".//item")[:limit]:
        title, link = txt(item.findtext("title", "")), (item.findtext("link", "") or "").strip()
        if title and link:
            src = item.find("source")
            out.append({"id": sid(title, link), "category": category, "title": title, "link": link,
                        "published": (item.findtext("pubDate", "") or "").strip(),
                        "source": txt(src.text) if src is not None and src.text else "News wire"})
    return category, out


def build_report(grouped, now):
    lines = [f"# Instant News Report — {now.strftime('%A, %B %d, %Y, %I:%M %p')}", "",
             f"**By Journalist {JOURNALIST}** — Toronto", ""]
    for cat, stories in grouped.items():
        if stories:
            lines += [f"## {cat}", ""] + [f"- {s['title']} ({s['source']}) — {s['link']}" for s in stories] + [""]
    lines += [f"---", f"*Reported instantly by Journalist {JOURNALIST}.*", ""]
    return "\n".join(lines)


def main() -> int:
    ap = argparse.ArgumentParser(description=f"Instant news reporter by {JOURNALIST}")
    ap.add_argument("--limit", type=int, default=5)
    ap.add_argument("--send", action="store_true", help="Email tip sites (needs NEWS_SMTP_* env)")
    args = ap.parse_args()
    clean_cache()
    now = datetime.now()
    print("Fetching all news in parallel ...")
    grouped = {}
    with ThreadPoolExecutor(max_workers=len(FEEDS)) as ex:
        for category, stories in ex.map(fetch, [(n, f, args.limit) for n, f in FEEDS]):
            grouped[category] = [s for s in stories
                                 if s["id"] not in {x["id"] for v in grouped.values() for x in v}]
    seen = json.loads(SEEN_FILE.read_text()) if SEEN_FILE.exists() else {}
    new = {c: [s for s in v if s["id"] not in seen] for c, v in grouped.items()}
    for c, v in grouped.items():
        for s in v:
            seen[s["id"]] = {"title": s["title"], "category": c, "first_seen": now.isoformat(timespec="seconds")}
    SEEN_FILE.write_text(json.dumps(seen, indent=2, ensure_ascii=False))
    display = new if sum(len(v) for v in new.values()) else grouped

    POSTS_DIR.mkdir(exist_ok=True); OUTBOX_DIR.mkdir(exist_ok=True)
    report_path = POSTS_DIR / f"instant_report_{now.strftime('%Y-%m-%d_%H%M')}.md"
    report_path.write_text(build_report(display, now), encoding="utf-8")
    report_text = report_path.read_text(encoding="utf-8")
    headlines = [s["title"] for v in display.values() for s in v][:8]

    subject = f"News report — {now.strftime('%B %d, %Y')} — Journalist {JOURNALIST}"
    body = (f"Hello,\n\nI am Journalist {JOURNALIST}, reporting from Toronto. "
            f"Here is my instant news report for {now.strftime('%A, %B %d, %Y')}.\n\n"
            + "\n".join(f"• {h}" for h in headlines)
            + f"\n\nFull report with sources:\n\n{report_text}\n— Journalist {JOURNALIST}\n")

    # Optional real sending
    smtp_ready = all(os.environ.get(k) for k in ("NEWS_SMTP_HOST", "NEWS_SMTP_USER", "NEWS_SMTP_PASS", "NEWS_FROM"))
    sent = set()
    if args.send and smtp_ready:
        with smtplib.SMTP(os.environ["NEWS_SMTP_HOST"], int(os.environ.get("NEWS_SMTP_PORT", "587"))) as smtp:
            smtp.starttls(); smtp.login(os.environ["NEWS_SMTP_USER"], os.environ["NEWS_SMTP_PASS"])
            for name, kind, addr in TIP_SITES:
                if kind == "email":
                    m = EmailMessage(); m["From"] = os.environ["NEWS_FROM"]; m["To"] = addr
                    m["Subject"] = subject; m.set_content(body); smtp.send_message(m); sent.add(name)

    index = [f"# Outbox — {now.strftime('%Y-%m-%d %H:%M')}", f"Journalist: {JOURNALIST}", ""]
    for name, kind, addr in TIP_SITES:
        f = OUTBOX_DIR / f"{name.lower().replace(' ', '_').replace('.', '')}_submission.txt"
        f.write_text(f"To: {addr}\nVia: {kind}\nSubject: {subject}\n\n{body}", encoding="utf-8")
        status = "SENT" if name in sent else ("ready to send" if kind == "email" else "ready — submit via web form")
        index.append(f"- [ ] **{name}** ({kind}: {addr}) — {status} — file: {f.name}")
    social = (f"📰 Instant News Report — {now.strftime('%B %d, %Y')}\nBy Journalist {JOURNALIST}\n\n"
              + "\n".join(f"• {h}" for h in headlines) + "\n\n#News #Toronto #Canada #JhamalSymister\n")
    (OUTBOX_DIR / "social_post.txt").write_text(social, encoding="utf-8")
    for s in SOCIAL_SITES:
        index.append(f"- [ ] **{s}** — ready to post — file: social_post.txt")
    index.append("- [x] **YouTube** — SKIPPED at Jay's request (Nov. 21, 2026)")
    (OUTBOX_DIR / "INDEX.md").write_text("\n".join(index) + "\n", encoding="utf-8")

    n_new = sum(len(v) for v in new.values()); n_all = sum(len(v) for v in grouped.values())
    print(f"Fetched: {n_all} | New: {n_new} | Sites prepared: {len(TIP_SITES) + len(SOCIAL_SITES)} | Emailed: {len(sent)}")
    print(f"Instant report: {report_path}")
    print(f"Outbox: {OUTBOX_DIR}/INDEX.md")
    if args.send and not smtp_ready:
        print("Note: --send needs NEWS_SMTP_* set; drafts were prepared instead, nothing was emailed.")
    clean_cache()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
