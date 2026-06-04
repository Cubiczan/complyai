"""
regulatory/ingest.py — Fetch and parse regulatory documents from US agencies.

Agencies supported:
  - SEC (EDGAR API — free, no key needed)
  - FinCEN (BSA/AML regulations — scrape fincen.gov)
  - CFPB (consumer protection rules — cfpb.gov API)
  - State regulators (NY DFS, CA DFPI, TX — hardcoded summaries)
"""

import json
import re
import sqlite3
from datetime import datetime, date
from pathlib import Path
from typing import Optional
from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup

# ─── Database ────────────────────────────────────────────────────────────────

DB_PATH = Path(__file__).parent.parent / "complyai.db"


def get_db() -> sqlite3.Connection:
    conn = sqlite3.connect(str(DB_PATH))
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA journal_mode=WAL")
    conn.execute("PRAGMA foreign_keys=ON")
    return conn


def init_db():
    """Initialize database schema. Safe to call multiple times."""
    conn = get_db()
    conn.executescript("""
        CREATE TABLE IF NOT EXISTS regulations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            agency TEXT NOT NULL,
            title TEXT NOT NULL,
            section TEXT,
            compliance_type TEXT NOT NULL,
            effective_date TEXT,
            summary TEXT NOT NULL,
            source_url TEXT,
            raw_text TEXT,
            ingested_at TEXT NOT NULL DEFAULT (datetime('now')),
            hash TEXT UNIQUE
        );
        CREATE INDEX IF NOT EXISTS idx_reg_agency ON regulations(agency);
        CREATE INDEX IF NOT EXISTS idx_reg_type ON regulations(compliance_type);
        CREATE INDEX IF NOT EXISTS idx_reg_effective ON regulations(effective_date);

        CREATE TABLE IF NOT EXISTS fintech_types (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT UNIQUE NOT NULL,
            display_name TEXT NOT NULL
        );

        CREATE TABLE IF NOT EXISTS fintech_type_regulations (
            fintech_type_id INTEGER REFERENCES fintech_types(id),
            regulation_id INTEGER REFERENCES regulations(id),
            priority INTEGER DEFAULT 0,
            PRIMARY KEY (fintech_type_id, regulation_id)
        );

        CREATE TABLE IF NOT EXISTS templates (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            slug TEXT UNIQUE NOT NULL,
            name TEXT NOT NULL,
            description TEXT,
            template_type TEXT NOT NULL,
            content TEXT NOT NULL,
            jurisdiction TEXT DEFAULT 'US',
            created_at TEXT NOT NULL DEFAULT (datetime('now'))
        );

        CREATE TABLE IF NOT EXISTS regulatory_changes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            regulation_id INTEGER REFERENCES regulations(id),
            change_type TEXT NOT NULL,
            old_hash TEXT,
            new_hash TEXT,
            summary TEXT NOT NULL,
            detected_at TEXT NOT NULL DEFAULT (datetime('now'))
        );

        CREATE TABLE IF NOT EXISTS crawl_log (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            agency TEXT NOT NULL,
            status TEXT NOT NULL,
            rules_found INTEGER DEFAULT 0,
            error_message TEXT,
            crawled_at TEXT NOT NULL DEFAULT (datetime('now'))
        );

        CREATE TABLE IF NOT EXISTS ingestion_cache (
            url TEXT PRIMARY KEY,
            content TEXT,
            fetched_at TEXT NOT NULL DEFAULT (datetime('now'))
        );
    """)
    conn.commit()
    conn.close()


def hash_text(text: str) -> str:
    """Simple content hash for change detection."""
    import hashlib
    return hashlib.sha256(text.encode("utf-8")).hexdigest()[:16]


def store_regulation(
    conn: sqlite3.Connection,
    agency: str,
    title: str,
    section: Optional[str],
    compliance_type: str,
    effective_date: Optional[str],
    summary: str,
    source_url: Optional[str] = None,
    raw_text: Optional[str] = None,
) -> Optional[int]:
    """Store a regulation, skipping duplicates by hash."""
    content_hash = hash_text(
        f"{agency}|{title}|{section}|{compliance_type}|{summary}"
    )
    try:
        cur = conn.execute(
            """INSERT INTO regulations
               (agency, title, section, compliance_type, effective_date,
                summary, source_url, raw_text, hash)
               VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)""",
            (agency, title, section, compliance_type, effective_date,
             summary, source_url, raw_text, content_hash),
        )
        return cur.lastrowid
    except sqlite3.IntegrityError:
        return None  # duplicate


def _get_text(el) -> str:
    return el.get_text(strip=True) if el else ""


# ─── SEC EDGAR ───────────────────────────────────────────────────────────────

SEC_BASE = "https://www.sec.gov"
SEC_SEARCH = (
    "https://efts.sec.gov/LATEST/search-index?q=%s&dateRange=custom"
    "&startdt=%s&enddt=%s&category=form-cat&location=edgar"
)


def ingest_sec(start_date: Optional[str] = None, end_date: Optional[str] = None) -> int:
    """Fetch recent SEC rule filings from EDGAR."""
    conn = get_db()
    count = 0

    end_date = end_date or date.today().isoformat()
    start_date = start_date or date(2025, 1, 1).isoformat()

    headers = {
        "User-Agent": "complyAI Research (shyamdesigan@gmail.com)",
        "Accept": "application/json",
    }

    try:
        # Search for recent rule filings
        resp = requests.get(
            SEC_SEARCH % ("rulemaking", start_date, end_date),
            headers=headers,
            timeout=30,
        )
        if resp.status_code != 200:
            _log_crawl(conn, "SEC", "error", error=f"HTTP {resp.status_code}")
            return 0

        data = resp.json()
        filings = data.get("hits", {}).get("hits", [])

        for hit in filings[:50]:  # limit to 50 per run
            source = hit.get("_source", {})
            title = source.get("title", "SEC Rulemaking Filing")
            summary = source.get("summary", "")
            form = source.get("form", "Rulemaking")
            effective = source.get("effective_date")

            reg_id = store_regulation(
                conn=conn,
                agency="SEC",
                title=title[:500],
                section=form,
                compliance_type="securities",
                effective_date=effective,
                summary=summary[:2000] if summary else "SEC rulemaking filing",
                source_url=(
                    urljoin(SEC_BASE, source.get("link", ""))
                    if source.get("link") else None
                ),
            )
            if reg_id:
                count += 1

        _log_crawl(conn, "SEC", "success", rules_found=count)
    except Exception as e:
        _log_crawl(conn, "SEC", "error", error=str(e))
        count = 0
    finally:
        conn.commit()
        conn.close()

    # Seed core SEC regulations even if API fails
    _seed_sec_core()
    return count


def _seed_sec_core():
    """Seed well-known SEC regulations that every fintech needs."""
    conn = get_db()
    seeded = [
        (
            "SEC",
            "Regulation D — Rule 506(b) and 506(c)",
            "Reg D",
            "securities",
            "2025-01-01",
            "Exemptions for private securities offerings. Rule 506(b) allows "
            "general solicitation with accredited investors only; 506(c) allows "
            "general solicitation with verification of accredited status.",
        ),
        (
            "SEC",
            "Regulation Crowdfunding — Regulation CF",
            "Reg CF",
            "securities",
            "2025-01-01",
            "Allows companies to raise up to $5M from retail investors through "
            "registered funding portals. Requires ongoing filings with EDGAR.",
        ),
        (
            "SEC",
            "Regulation A+ — Tier 1 and Tier 2",
            "Reg A+",
            "securities",
            "2025-01-01",
            "Mini-IPO exemption. Tier 1: up to $20M (state review required). "
            "Tier 2: up to $75M (federal review only, ongoing reporting).",
        ),
        (
            "SEC",
            "Investment Advisers Act of 1940",
            "IA-1940",
            "securities",
            "1940-01-01",
            "Registration and regulation of investment advisers. Requires "
            "registration with SEC if managing $100M+ AUM. State registration below.",
        ),
        (
            "SEC",
            "Securities Exchange Act of 1934 — Section 10(b) and Rule 10b-5",
            "1934-Act",
            "securities",
            "1934-01-01",
            "Anti-fraud provisions. Prohibits deceptive practices in connection "
            "with securities transactions. Applies to all fintechs dealing with securities.",
        ),
    ]
    for agency, title, section, ctype, effective, summary in seeded:
        store_regulation(conn, agency, title, section, ctype, effective, summary)
    conn.commit()
    conn.close()


# ─── FinCEN ──────────────────────────────────────────────────────────────────

FINCEN_URL = "https://www.fincen.gov/resources/statutes-regulations"


def ingest_fincen() -> int:
    """Scrape FinCEN for BSA/AML regulations."""
    conn = get_db()
    count = 0

    try:
        resp = requests.get(
            FINCEN_URL,
            headers={"User-Agent": "complyAI/1.0"},
            timeout=30,
        )
        if resp.status_code != 200:
            _log_crawl(conn, "FinCEN", "error", error=f"HTTP {resp.status_code}")
            return 0

        soup = BeautifulSoup(resp.text, "html.parser")
        links = soup.select("a[href*='/resources/']")
        seen = set()

        for link in links:
            href = link.get("href", "").strip()
            text = link.get_text(strip=True)
            if not href or not text or href in seen:
                continue
            seen.add(href)
            if len(seen) > 30:
                break

            full_url = urljoin("https://www.fincen.gov", href) if href.startswith("/") else href
            reg_id = store_regulation(
                conn=conn,
                agency="FinCEN",
                title=text[:500],
                section="BSA/AML",
                compliance_type="aml",
                effective_date=None,
                summary=f"FinCEN regulation: {text}",
                source_url=full_url,
            )
            if reg_id:
                count += 1

        _log_crawl(conn, "FinCEN", "success", rules_found=count)
    except Exception as e:
        _log_crawl(conn, "FinCEN", "error", error=str(e))
        count = 0
    finally:
        conn.commit()
        conn.close()

    _seed_fincen_core()
    return count


def _seed_fincen_core():
    conn = get_db()
    seeded = [
        (
            "FinCEN",
            "Bank Secrecy Act (BSA)",
            "BSA",
            "aml",
            "1970-01-01",
            "Core anti-money laundering law. Requires financial institutions to "
            "maintain AML programs, file SARs (Suspicious Activity Reports), "
            "and CTRs (Currency Transaction Reports).",
        ),
        (
            "FinCEN",
            "AML Program Requirements — 31 CFR § 1020.210",
            "31 CFR § 1020.210",
            "aml",
            "2021-01-01",
            "Requires banks to establish written AML programs including: "
            "(1) policies/procedures, (2) designated compliance officer, "
            "(3) ongoing training, (4) independent audit.",
        ),
        (
            "FinCEN",
            "Customer Due Diligence Rule — 31 CFR § 1010.230",
            "31 CFR § 1010.230",
            "aml",
            "2018-05-11",
            "Requires covered financial institutions to identify beneficial "
            "owners of legal entity customers (25%+ ownership).",
        ),
        (
            "FinCEN",
            "Corporate Transparency Act (CTA) Beneficial Ownership Reporting",
            "CTA-BOI",
            "aml",
            "2024-01-01",
            "Requires reporting companies to file beneficial ownership "
            "information with FinCEN. Applies to most LLCs and corporations.",
        ),
        (
            "FinCEN",
            "Suspicious Activity Report (SAR) Requirements",
            "SAR",
            "aml",
            "2023-01-01",
            "Requires filing SARs for transactions over $5,000 involving "
            "suspected illegal activity. Filing deadline: 30 days (extendable to 60).",
        ),
    ]
    for agency, title, section, ctype, effective, summary in seeded:
        store_regulation(conn, agency, title, section, ctype, effective, summary)
    conn.commit()
    conn.close()


# ─── CFPB ────────────────────────────────────────────────────────────────────

CFPB_API = "https://www.consumerfinance.gov/api/"
CFPB_RULES = "https://www.consumerfinance.gov/rules-policy/final-rules/"


def ingest_cfpb() -> int:
    """Fetch CFPB consumer protection rules via their public API."""
    conn = get_db()
    count = 0

    try:
        resp = requests.get(
            CFPB_RULES,
            headers={"User-Agent": "complyAI/1.0"},
            timeout=30,
        )
        if resp.status_code != 200:
            _log_crawl(conn, "CFPB", "error", error=f"HTTP {resp.status_code}")
            return 0

        soup = BeautifulSoup(resp.text, "html.parser")
        rule_items = soup.select("article, .rule-item, .post-preview")
        if not rule_items:
            rule_items = soup.select("a[href*='/rules-policy/final-rules/']")

        seen = set()
        for item in rule_items:
            if isinstance(item, BeautifulSoup):
                tag = item
            else:
                tag = item

            title_el = tag.select_one("h2, h3, .title")
            link_el = tag.select_one("a") if tag.name == "a" else tag.select_one("a[href]")
            if not title_el and not link_el:
                continue

            title = title_el.get_text(strip=True) if title_el else (
                link_el.get_text(strip=True) if link_el else "CFPB Final Rule"
            )
            href = link_el.get("href", "") if link_el else ""
            if href in seen:
                continue
            seen.add(href)
            if len(seen) > 30:
                break

            full_url = urljoin("https://www.consumerfinance.gov", href) if href.startswith("/") else href or CFPB_RULES

            reg_id = store_regulation(
                conn=conn,
                agency="CFPB",
                title=title[:500],
                section="Consumer Protection",
                compliance_type="consumer_protection",
                effective_date=None,
                summary=f"CFPB consumer protection rule: {title[:300]}",
                source_url=full_url,
            )
            if reg_id:
                count += 1

        _log_crawl(conn, "CFPB", "success", rules_found=count)
    except Exception as e:
        _log_crawl(conn, "CFPB", "error", error=str(e))
        count = 0
    finally:
        conn.commit()
        conn.close()

    _seed_cfpb_core()
    return count


def _seed_cfpb_core():
    conn = get_db()
    seeded = [
        (
            "CFPB",
            "Regulation E — Electronic Fund Transfers (12 CFR 1005)",
            "Reg E",
            "consumer_protection",
            "2024-07-01",
            "Governs electronic fund transfers: debit cards, ACH, payroll, "
            "and prepaid accounts. Requires error resolution, limited liability "
            "for unauthorized transfers, and monthly statements.",
        ),
        (
            "CFPB",
            "Regulation Z — Truth in Lending Act (12 CFR 1026)",
            "Reg Z",
            "consumer_protection",
            "2024-10-01",
            "Consumer lending disclosures: APR, finance charges, total payments, "
            "payment schedule. Applies to credit cards, mortgages, personal loans. "
            "Includes ability-to-repay requirements.",
        ),
        (
            "CFPB",
            "Remittance Transfer Rule — 12 CFR 1005 Subpart B",
            "Remittance",
            "consumer_protection",
            "2020-07-01",
            "Disclosure requirements for international money transfers. Requires "
            "disclosure of exchange rate, fees, and delivery date. Right to cancel.",
        ),
        (
            "CFPB",
            "Prepaid Accounts Rule — 12 CFR 1005 Subpart A",
            "Prepaid",
            "consumer_protection",
            "2022-06-01",
            "Regulation E extended to prepaid accounts. Requires upfront "
            "disclosure of fees, access to account history, and error resolution.",
        ),
        (
            "CFPB",
            "Small Business Lending Rule — 12 CFR 1002",
            "Small Biz Lending",
            "consumer_protection",
            "2025-01-01",
            "Section 1071 of Dodd-Frank. Requires collection of small business "
            "credit application data including demographics and pricing.",
        ),
        (
            "CFPB",
            "Debt Collection Rule — Reg F (12 CFR 1006)",
            "Reg F",
            "consumer_protection",
            "2021-11-30",
            "Fair Debt Collection Practices Act implementation. Limits call "
            "frequency (7 calls in 7 days), requires electronic disclosure, "
            "and sets validation notice requirements.",
        ),
    ]
    for agency, title, section, ctype, effective, summary in seeded:
        store_regulation(conn, agency, title, section, ctype, effective, summary)
    conn.commit()
    conn.close()


# ─── State Regulators ────────────────────────────────────────────────────────


STATE_REGULATORS = {
    "NY": {
        "name": "New York Department of Financial Services (NY DFS)",
        "url": "https://www.dfs.ny.gov",
        "regulations": [
            {
                "title": "NYDFS Cybersecurity Regulation (23 NYCRR 500)",
                "section": "23 NYCRR 500",
                "compliance_type": "cybersecurity",
                "effective_date": "2024-11-01",
                "summary": "Requires financial services companies to maintain a "
                "cybersecurity program, designate a CISO, implement multi-factor "
                "authentication, conduct annual risk assessments, and notify DFS "
                "of cybersecurity events within 72 hours.",
            },
            {
                "title": "NY BitLicense — Virtual Currency Regulation (23 NYCRR 200)",
                "section": "23 NYCRR 200",
                "compliance_type": "crypto",
                "effective_date": "2015-08-08",
                "summary": "Requires businesses engaging in virtual currency "
                "activities in New York to obtain a BitLicense. Covers custody, "
                "transaction monitoring, consumer protection, and capital requirements.",
            },
            {
                "title": "NY Money Transmitter Law — Article XIII-B of Banking Law",
                "section": "NY Banking Law Article XIII-B",
                "compliance_type": "money_transmission",
                "effective_date": "2023-07-01",
                "summary": "Requires license for money transmission in NY. "
                "Includes net worth requirements ($500K-$2M), surety bond, "
                "and permissible investments requirements.",
            },
        ],
    },
    "CA": {
        "name": "California Department of Financial Protection and Innovation (CA DFPI)",
        "url": "https://dfpi.ca.gov",
        "regulations": [
            {
                "title": "California Consumer Financial Protection Law (CCFPL)",
                "section": "CA Financial Code Div 24",
                "compliance_type": "consumer_protection",
                "effective_date": "2021-01-01",
                "summary": "Grants DFPI enforcement authority over consumer "
                "financial products. Prohibits unfair, deceptive, or abusive "
                "acts (UDAAP). Requires registration for covered persons.",
            },
            {
                "title": "California Money Transmission Act",
                "section": "CA Financial Code Div 1.2",
                "compliance_type": "money_transmission",
                "effective_date": "2023-07-01",
                "summary": "Requires license for money transmission in California. "
                "Updated 2023 to align with federal model. Net worth, surety bond, "
                "and reporting requirements.",
            },
            {
                "title": "California Consumer Privacy Act (CCPA) — Financial Data",
                "section": "CCPA",
                "compliance_type": "privacy",
                "effective_date": "2023-01-01",
                "summary": "Consumer privacy rights including right to know, "
                "delete, and opt-out of sale of personal information. Financial "
                "institutions must comply with CCPA in addition to GLBA.",
            },
            {
                "title": "California Student Loan Servicing Act",
                "section": "CA Fin Code § 28100",
                "compliance_type": "lending",
                "effective_date": "2020-01-01",
                "summary": "Requires licensure for student loan servicers. "
                "Includes reporting, recordkeeping, and examination requirements.",
            },
        ],
    },
    "TX": {
        "name": "Texas Department of Banking",
        "url": "https://www.dob.texas.gov",
        "regulations": [
            {
                "title": "Texas Money Services Act (TMSA)",
                "section": "TX Fin Code Ch 151-157",
                "compliance_type": "money_transmission",
                "effective_date": "2023-01-01",
                "summary": "License required for money transmission and currency "
                "exchange. Net worth: $50K-$500K depending on volume. Surety "
                "bond required. Includes virtual currency guidance.",
            },
            {
                "title": "Texas Lending Requirements",
                "section": "TX Fin Code Ch 341-351",
                "compliance_type": "lending",
                "effective_date": "2023-01-01",
                "summary": "Regulates consumer loans, credit access businesses. "
                "Interest rate limits, disclosure requirements, and licensing for "
                "certain lending activities. Regulated by Office of Consumer Credit.",
            },
        ],
    },
}


def ingest_state_regulators(states: Optional[list[str]] = None) -> int:
    """Ingest hardcoded state regulator summaries."""
    conn = get_db()
    count = 0

    target_states = states or list(STATE_REGULATORS.keys())

    for state_code in target_states:
        if state_code not in STATE_REGULATORS:
            continue
        info = STATE_REGULATORS[state_code]
        for reg in info["regulations"]:
            reg_id = store_regulation(
                conn=conn,
                agency=f"{state_code} — {info['name']}",
                title=reg["title"],
                section=reg.get("section"),
                compliance_type=reg["compliance_type"],
                effective_date=reg.get("effective_date"),
                summary=reg["summary"],
                source_url=info.get("url"),
            )
            if reg_id:
                count += 1

    conn.commit()
    conn.close()
    return count


def ingest_all_states() -> int:
    """Ingest all hardcoded state regulator summaries."""
    return ingest_state_regulators()


# ─── Crawl Logging ───────────────────────────────────────────────────────────


def _log_crawl(
    conn: sqlite3.Connection,
    agency: str,
    status: str,
    rules_found: int = 0,
    error: Optional[str] = None,
):
    conn.execute(
        """INSERT INTO crawl_log (agency, status, rules_found, error_message)
           VALUES (?, ?, ?, ?)""",
        (agency, status, rules_found, error),
    )


# ─── All-in-One ──────────────────────────────────────────────────────────────


def ingest_all() -> dict[str, int]:
    """Run all ingestion sources. Returns counts per agency."""
    init_db()
    results = {
        "SEC": ingest_sec(),
        "FinCEN": ingest_fincen(),
        "CFPB": ingest_cfpb(),
        "State_Regulators": ingest_all_states(),
    }
    return results


def get_regulations(
    agency: Optional[str] = None,
    compliance_type: Optional[str] = None,
    limit: int = 100,
) -> list[dict]:
    """Query stored regulations with optional filters."""
    conn = get_db()
    query = "SELECT * FROM regulations WHERE 1=1"
    params = []

    if agency:
        query += " AND agency LIKE ?"
        params.append(f"%{agency}%")
    if compliance_type:
        query += " AND compliance_type = ?"
        params.append(compliance_type)

    query += " ORDER BY effective_date DESC NULLS LAST LIMIT ?"
    params.append(limit)

    rows = conn.execute(query, params).fetchall()
    conn.close()
    return [dict(r) for r in rows]


if __name__ == "__main__":
    init_db()
    results = ingest_all()
    print(f"✅ Ingestion complete: {results}")
    print(f"Total regulations in DB: {len(get_regulations())}")
