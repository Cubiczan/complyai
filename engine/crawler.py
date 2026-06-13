"""
engine/crawler.py — Daily crawler for regulatory updates and changes.

Checks SEC, CFPB, and FINRA feeds for new or updated regulations.
Stores changes for the monitor to process.
"""

from datetime import datetime, date, timedelta
from typing import Optional
import logging
import sqlite3
from pathlib import Path

import requests
from bs4 import BeautifulSoup

from cubiczan_resilience import resilient

logger = logging.getLogger("complyai.crawler")


@resilient(timeout=30, max_attempts=3)
def _fetch_feed_raw(url: str, timeout: int = 30) -> requests.Response:
    """Fetch a feed URL with retry + exponential backoff + jitter + circuit breaker."""
    headers = {"User-Agent": "complyAI-Crawler/1.0"}
    resp = requests.get(url, headers=headers, timeout=timeout)
    resp.raise_for_status()
    return resp

from engine.ingest import (
    get_db,
    ingest_sec,
    ingest_fincen,
    ingest_cfpb,
    ingest_state_regulators,
    _log_crawl,
    init_db,
)

DB_PATH = Path(__file__).parent.parent / "complyai.db"


# ─── Feed URLs ───────────────────────────────────────────────────────────────

FEEDS = {
    "SEC_Rulemaking": "https://www.sec.gov/rss/rulemaking.xml",
    "SEC_Investor_Alerts": "https://www.sec.gov/rss/investor-alerts.xml",
    "CFPB_Feed": "https://www.consumerfinance.gov/about-us/newsroom/feed.xml",
    "FINRA_Regulatory": "https://www.finra.org/rss/regulatory-notices.xml",
}

CACHE_EXPIRY_HOURS = 24  # Re-fetch after this many hours


# ─── Feed Fetcher ────────────────────────────────────────────────────────────


def fetch_feed(url: str, timeout: int = 30) -> Optional[list[dict]]:
    """Fetch and parse an RSS/Atom feed into entries."""
    try:
        resp = _fetch_feed_raw(url, timeout=timeout)

        soup = BeautifulSoup(resp.content, "xml")
        entries = []

        # Try RSS items
        for item in soup.select("item"):
            entry = {
                "title": _safe(item, "title"),
                "link": _safe(item, "link"),
                "description": _safe(item, "description"),
                "pub_date": _safe(item, "pubDate"),
                "guid": _safe(item, "guid"),
            }
            if entry["title"]:
                entries.append(entry)

        # Try Atom entries
        for entry in soup.select("entry"):
            link_el = entry.select_one("link")
            link = link_el.get("href", "") if link_el else ""
            entry_data = {
                "title": _safe(entry, "title"),
                "link": link,
                "description": _safe(entry, "content") or _safe(entry, "summary"),
                "pub_date": _safe(entry, "published") or _safe(entry, "updated"),
                "guid": _safe(entry, "id"),
            }
            if entry_data["title"]:
                entries.append(entry_data)

        return entries[:20]  # limit per feed

    except requests.RequestException as e:
        logger.warning("Feed fetch failed after retries (%s): %s", url[:60], e)
        print(f"  ⚠️  Feed fetch failed ({url[:60]}...): {e}")
        return None
    except Exception as e:
        logger.warning("Feed fetch/parse error (%s): %s", url[:60], e)
        print(f"  ⚠️  Feed parse error ({url[:60]}...): {e}")
        return None


def _safe(soup, tag: str) -> str:
    el = soup.find(tag)
    return el.text.strip() if el and el.text else ""


# ─── Cache Check ─────────────────────────────────────────────────────────────


def is_feed_cached(url: str) -> bool:
    """Check if a feed was fetched recently."""
    conn = get_db()
    row = conn.execute(
        """SELECT fetched_at FROM ingestion_cache WHERE url = ?""",
        (url,),
    ).fetchone()
    conn.close()

    if row:
        fetched = datetime.fromisoformat(row["fetched_at"])
        age_hours = (datetime.utcnow() - fetched).total_seconds() / 3600
        return age_hours < CACHE_EXPIRY_HOURS
    return False


def cache_feed(url: str, content: str):
    """Store fetched feed content with timestamp."""
    conn = get_db()
    conn.execute(
        """INSERT OR REPLACE INTO ingestion_cache (url, content, fetched_at)
           VALUES (?, ?, datetime('now'))""",
        (url, content),
    )
    conn.commit()
    conn.close()


# ─── Crawl Dispatchers ───────────────────────────────────────────────────────


def crawl_feeds() -> int:
    """Check all regulatory RSS feeds for new items."""
    print(f"🔍 Crawling regulatory feeds ({datetime.utcnow().isoformat()})")
    total_new = 0

    for name, url in FEEDS.items():
        if is_feed_cached(url):
            print(f"  📦 Skipping {name} (cached)")
            continue

        entries = fetch_feed(url)
        if entries is None:
            continue

        print(f"  📰 {name}: {len(entries)} entries found")
        cache_feed(url, str(entries))
        total_new += len(entries)

    return total_new


def crawl_all(force: bool = False) -> dict[str, int]:
    """Run all ingestion and feed crawling. Returns counts."""
    init_db()
    results = {
        "feeds": crawl_feeds(),
    }

    # Always run ingestion (it deduplicates by hash)
    print("📥 Running agency ingestion...")
    for agency_name, fn in [
        ("SEC", ingest_sec),
        ("FinCEN", ingest_fincen),
        ("CFPB", ingest_cfpb),
    ]:
        print(f"  ⚙️  {agency_name}...")
        cnt = fn()
        results[agency_name] = cnt
        print(f"     → {cnt} regulations ingested")

    print(f"  ⚙️  State Regulators...")
    cnt = ingest_state_regulators()
    results["State_Regulators"] = cnt

    return results


# ─── Change Detection (Run after ingestion) ──────────────────────────────────


def detect_changes() -> list[dict]:
    """Compare latest ingestion against previous run. Returns changes."""
    conn = get_db()
    changes = []

    # Get regulations ingested in the last crawl
    latest_crawl = conn.execute(
        """SELECT MAX(crawled_at) as last_time FROM crawl_log
           WHERE status = 'success'""",
    ).fetchone()
    if not latest_crawl or not latest_crawl["last_time"]:
        conn.close()
        return []

    # Get the previous successful crawl time
    prev_crawl = conn.execute(
        """SELECT MAX(crawled_at) as prev_time FROM crawl_log
           WHERE status = 'success'
             AND crawled_at < ?""",
        (latest_crawl["last_time"],),
    ).fetchone()

    if not prev_crawl or not prev_crawl["prev_time"]:
        conn.close()
        return []

    # Any new regulations since last crawl?
    new_regs = conn.execute(
        """SELECT * FROM regulations
           WHERE ingested_at > ?
           ORDER BY ingested_at DESC""",
        (prev_crawl["prev_time"],),
    ).fetchall()

    for reg in new_regs:
        changes.append({
            "type": "new_regulation",
            "agency": reg["agency"],
            "title": reg["title"],
            "summary": reg["summary"][:200],
            "detected_at": datetime.utcnow().isoformat(),
        })

    conn.close()
    return changes


# ─── CLI ──────────────────────────────────────────────────────────────────────


def run_daily():
    """Full daily crawl: fetch, ingest, detect changes."""
    print("=" * 60)
    print("complyAI Daily Regulatory Crawl")
    print(f"Started: {datetime.utcnow().isoformat()}")
    print("=" * 60)

    results = crawl_all(force=False)
    print(f"\n📊 Results: {results}")

    changes = detect_changes()
    print(f"\n🔔 Changes detected: {len(changes)}")
    for c in changes:
        print(f"  • {c['agency']}: {c['title'][:80]}...")

    print(f"\n✅ Crawl complete at {datetime.utcnow().isoformat()}")
    return results


if __name__ == "__main__":
    run_daily()
