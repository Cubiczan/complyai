"""
monitor/watcher.py — Watch regulatory feeds for changes and updates.

Checks SEC, CFPB, and FINRA feeds on a schedule and flags new or
updated regulations for review.
"""

from datetime import datetime, date, timedelta
from typing import Optional
import sqlite3
from pathlib import Path

import requests
from bs4 import BeautifulSoup

from engine.ingest import get_db, _log_crawl

DB_PATH = Path(__file__).parent.parent / "complyai.db"

# ─── Watch Targets ───────────────────────────────────────────────────────────

WATCH_FEEDS = {
    "SEC_What_s_New": "https://www.sec.gov/rss/whatsnew.xml",
    "SEC_Proposed_Rules": "https://www.sec.gov/rss/proposed.xml",
    "SEC_Final_Rules": "https://www.sec.gov/rss/final.xml",
    "CFPB_Final_Rules": "https://www.consumerfinance.gov/rules-policy/final-rules/feed.xml",
    "FINRA_Notices": "https://www.finra.org/rss/regulatory-notices.xml",
}

ALERTS_URLS = {
    "SEC_Investor_Alerts": "https://www.sec.gov/page/investor-alerts-and-bulletins",
    "FFIEC_News": "https://www.ffiec.gov/press/feed.xml",
}


def fetch_feed_items(url: str, max_items: int = 10) -> list[dict]:
    """Fetch and parse RSS/Atom feed items."""
    items = []
    try:
        headers = {"User-Agent": "complyAI-Watcher/1.0 (shyamdesigan@gmail.com)"}
        resp = requests.get(url, headers=headers, timeout=20)
        resp.raise_for_status()

        soup = BeautifulSoup(resp.content, "xml" if "xml" in resp.headers.get("content-type", "") else "html.parser")

        # RSS items
        for item in soup.select("item")[:max_items]:
            entry = {
                "title": _safe(item, "title"),
                "link": _safe(item, "link"),
                "description": _safe(item, "description"),
                "pub_date": _safe(item, "pubDate"),
                "guid": _safe(item, "guid"),
            }
            if entry["title"]:
                items.append(entry)

        # Atom entries
        for entry in soup.select("entry")[:max_items]:
            link_el = entry.select_one("link")
            items.append({
                "title": _safe(entry, "title"),
                "link": link_el.get("href", "") if link_el else "",
                "description": _safe(entry, "content") or _safe(entry, "summary"),
                "pub_date": _safe(entry, "published") or _safe(entry, "updated"),
                "guid": _safe(entry, "id"),
            })

    except requests.RequestException as e:
        print(f"  ⚠️  Watch feed error ({url[:60]}...): {e}")
    except Exception as e:
        print(f"  ⚠️  Feed parse error: {e}")

    return items


def _safe(soup, tag: str) -> str:
    el = soup.find(tag)
    return el.text.strip() if el and el.text else ""


def check_feeds() -> list[dict]:
    """Check all watch feeds and return new items."""
    now = datetime.utcnow()
    new_items = []

    print(f"🔍 Checking regulatory feeds ({now.isoformat()})")

    for name, url in WATCH_FEEDS.items():
        items = fetch_feed_items(url)
        if not items:
            print(f"  ⚙️  {name}: no items found")
            continue

        print(f"  📰 {name}: {len(items)} items")

        for item in items:
            item["feed_name"] = name
            item["detected_at"] = now.isoformat()
            new_items.append(item)

    return new_items


def watch() -> list[dict]:
    """Full watch cycle — check feeds, log results, return changes."""
    conn = get_db()

    new_items = check_feeds()
    _log_crawl(conn, "WATCHER", "success", rules_found=len(new_items))

    # Store new items as regulatory changes
    for item in new_items:
        conn.execute(
            """INSERT OR IGNORE INTO regulatory_changes
               (regulation_id, change_type, summary, detected_at)
               VALUES (NULL, 'feed_update', ?, ?)""",
            (
                f"[{item['feed_name']}] {item['title'][:300]}",
                item["detected_at"],
            ),
        )

    conn.commit()
    conn.close()
    return new_items


if __name__ == "__main__":
    results = watch()
    print(f"\n✅ Watcher checked {len(WATCH_FEEDS)} feeds, found {len(results)} items")
    for r in results[:5]:
        print(f"  • {r['feed_name']}: {r['title'][:80]}")
