"""
regulatory/parser.py — Parse HTML/PDF into structured rules.

Converts raw regulatory text into structured records with:
  - agency
  - title
  - section
  - compliance_type
  - effective_date
  - summary

Supports both inline parsing of scraped HTML and PDF text extraction.
"""

import re
from datetime import datetime
from typing import Optional


# ─── Parsed Regulation Model ─────────────────────────────────────────────────

class ParsedRegulation:
    """A single parsed regulation entry."""

    def __init__(
        self,
        agency: str,
        title: str,
        section: Optional[str] = None,
        compliance_type: str = "general",
        effective_date: Optional[str] = None,
        summary: str = "",
        source_url: Optional[str] = None,
        raw_text: Optional[str] = None,
    ):
        self.agency = agency.strip()
        self.title = title.strip()
        self.section = section.strip() if section else None
        self.compliance_type = compliance_type.strip()
        self.effective_date = effective_date
        self.summary = summary.strip()
        self.source_url = source_url
        self.raw_text = raw_text[:5000] if raw_text else None

    def to_dict(self) -> dict:
        return {
            "agency": self.agency,
            "title": self.title,
            "section": self.section,
            "compliance_type": self.compliance_type,
            "effective_date": self.effective_date,
            "summary": self.summary,
            "source_url": self.source_url,
        }

    def __repr__(self) -> str:
        return f"<ParsedRegulation {self.agency}:{self.title[:50]}...>"


# ─── Rule Pattern Extraction ─────────────────────────────────────────────────

# Common patterns for identifying regulation titles and sections
TITLE_PATTERNS = [
    # "Title X — ..." or "Title X: ..."
    r"Title\s+(?:IV\b|[A-Z]+|\d+)\s*[:\u2014-]\s*[A-Z][A-Za-z\s,]+",
    # "Regulation [A-Z]"
    r"Regulation\s+[A-Z]\b",
    # "Section XXXX.XX"
    r"Section\s+\d{3,4}\.\d+\b",
    # "Part XXXX"
    r"Part\s+\d{3,4}\b",
    # "12 CFR 10XX" or "31 CFR 10XX"
    r"\d{2}\s+CFR\s+\d+\.?\d*",
    # "Public Law XXX-XXX"
    r"Public\s+Law\s+\d{2,3}-\d{1,3}",
]

COMPLIANCE_KEYWORDS = {
    "anti-money laundering": "aml",
    "money laundering": "aml",
    "bsa": "aml",
    "bank secrecy act": "aml",
    "suspicious activity": "aml",
    "currency transaction": "aml",
    "know your customer": "aml",
    "kyc": "aml",
    "aml": "aml",
    "consumer protection": "consumer_protection",
    "truth in lending": "consumer_protection",
    "electronic fund transfer": "consumer_protection",
    "regulation e": "consumer_protection",
    "regulation z": "consumer_protection",
    "debt collection": "consumer_protection",
    "fair lending": "consumer_protection",
    "remittance": "consumer_protection",
    "securities": "securities",
    "rule 506": "securities",
    "regulation d": "securities",
    "regulation cf": "securities",
    "investment advisers": "securities",
    "cybersecurity": "cybersecurity",
    "data privacy": "privacy",
    "ccpa": "privacy",
    "gdpr": "privacy",
    "glba": "privacy",
    "gramm-leach-bliley": "privacy",
    "money transmission": "money_transmission",
    "money transmitter": "money_transmission",
    "bitlicense": "crypto",
    "virtual currency": "crypto",
    "crypto": "crypto",
    "digital asset": "crypto",
    "lending": "lending",
    "credit": "lending",
    "loan": "lending",
    "payday": "lending",
    "student loan": "lending",
}

DATE_PATTERNS = [
    r"effective\s+(?:on\s+)?([A-Z][a-z]+ \d{1,2},?\s*\d{4})",
    r"effective\s+date[:\s]+([A-Z][a-z]+ \d{1,2},?\s*\d{4})",
    r"(?:January|February|March|April|May|June|July|August|September|October|November|December)\s+\d{1,2},?\s*\d{4}",
    r"\d{2}/\d{2}/\d{4}",
    r"\d{4}-\d{2}-\d{2}",
]


def detect_compliance_type(text: str) -> str:
    """Detect the compliance type from text using keyword matching."""
    text_lower = text.lower()
    for keyword, ctype in COMPLIANCE_KEYWORDS.items():
        if keyword in text_lower:
            return ctype
    return "general"


def extract_title(text: str) -> Optional[str]:
    """Extract a regulation title from text."""
    for pattern in TITLE_PATTERNS:
        match = re.search(pattern, text)
        if match:
            return match.group(0)
    return None


def extract_date(text: str) -> Optional[str]:
    """Extract earliest date from text."""
    for pattern in DATE_PATTERNS:
        for match in re.finditer(pattern, text, re.IGNORECASE):
            date_str = match.group(0).strip()
            # Clean up
            date_str = re.sub(r"\s+", " ", date_str)
            date_str = date_str.rstrip(",")
            try:
                # Try parsing various formats
                for fmt in [
                    "%B %d, %Y",
                    "%B %d %Y",
                    "%m/%d/%Y",
                    "%Y-%m-%d",
                ]:
                    try:
                        parsed = datetime.strptime(date_str, fmt)
                        return parsed.strftime("%Y-%m-%d")
                    except ValueError:
                        continue
            except Exception:
                continue
    return None


def clean_html_text(html: str) -> str:
    """Remove HTML tags and normalize whitespace for parsing."""
    text = re.sub(r"<[^>]+>", " ", html)
    text = re.sub(r"\s+", " ", text)
    text = re.sub(r"\n\s*\n", "\n\n", text)
    return text.strip()


# ─── Main Parser ─────────────────────────────────────────────────────────────


def parse_regulation(
    text: str,
    source_agency: str = "Unknown",
    source_url: Optional[str] = None,
) -> Optional[ParsedRegulation]:
    """Parse raw text into a structured ParsedRegulation."""
    if not text or len(text.strip()) < 20:
        return None

    clean = clean_html_text(text) if "<" in text else text
    # Take first 2000 chars for analysis
    head = clean[:2000]

    title = extract_title(head)
    if not title:
        # Use first sentence as title
        first_sentence = re.split(r'[.!?]', head.strip())[0]
        title = first_sentence[:200] if first_sentence else "Regulation"

    compliance_type = detect_compliance_type(head)
    effective_date = extract_date(head)

    # Generate summary: first few sentences
    sentences = re.split(r'(?<=[.!?])\s+', clean[:1000])
    summary = " ".join(sentences[:3]) if sentences else clean[:500]

    return ParsedRegulation(
        agency=source_agency,
        title=title[:500],
        section=None,
        compliance_type=compliance_type,
        effective_date=effective_date,
        summary=summary[:2000],
        source_url=source_url,
        raw_text=clean,
    )


def parse_regulations_bulk(
    texts: list[tuple[str, str, Optional[str]]],
) -> list[ParsedRegulation]:
    """Parse multiple texts. Each tuple: (text, agency, url_or_none)."""
    results = []
    for text, agency, url in texts:
        parsed = parse_regulation(text, agency, url)
        if parsed:
            results.append(parsed)
    return results


# ─── PDF Text Extraction (Simple) ────────────────────────────────────────────


def extract_pdf_text(pdf_path: str) -> Optional[str]:
    """Extract text from a PDF file. Requires PyMuPDF or pdfminer."""
    try:
        import fitz  # PyMuPDF
        doc = fitz.open(pdf_path)
        text = ""
        for page in doc:
            text += page.get_text()
        doc.close()
        return text
    except ImportError:
        pass

    try:
        from pdfminer.high_level import extract_text
        text = extract_text(pdf_path)
        return text
    except ImportError:
        pass

    try:
        import subprocess
        result = subprocess.run(
            ["pdftotext", pdf_path, "-"],
            capture_output=True, text=True, timeout=30,
        )
        if result.returncode == 0 and result.stdout.strip():
            return result.stdout
    except FileNotFoundError:
        pass
    except Exception:
        pass

    return None


if __name__ == "__main__":
    # Quick test
    sample = """
    Regulation E — Electronic Fund Transfers (12 CFR 1005)
    Effective January 1, 2024
    
    This regulation governs electronic fund transfers including debit cards,
    ACH transfers, and prepaid accounts. It requires financial institutions
    to provide error resolution procedures and limits consumer liability
    for unauthorized transfers.
    
    Section 1005.6 — Liability of Consumer for Unauthorized Transfers
    A consumer's liability for an unauthorized electronic fund transfer
    is limited to $50 if reported within 2 business days.
    """
    
    parsed = parse_regulation(sample, "CFPB", "https://example.com/reg-e")
    if parsed:
        print(f"Agency: {parsed.agency}")
        print(f"Title: {parsed.title}")
        print(f"Type: {parsed.compliance_type}")
        print(f"Date: {parsed.effective_date}")
        print(f"Summary: {parsed.summary[:200]}...")
