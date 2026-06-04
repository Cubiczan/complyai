"""
monitor/notify.py — Generate change notification reports.

Creates structured reports of regulatory changes, filtered by fintech
type, for email or in-app notifications.
"""

from datetime import datetime, timedelta
from typing import Optional
import sqlite3
from pathlib import Path

from engine.ingest import get_db
from checklist.types import get_regulations_for_type, FINTECH_TYPES

DB_PATH = Path(__file__).parent.parent / "complyai.db"

TYPES_BY_CATEGORY = {
    "AML": ["payments", "lending", "crypto", "p2p", "banking", "wealth"],
    "Consumer Protection": ["payments", "lending", "crypto", "p2p", "banking", "wealth", "insurance"],
    "Securities": ["wealth", "crypto"],
    "Privacy": ["payments", "lending", "crypto", "p2p", "banking", "wealth", "insurance"],
    "Cybersecurity": ["payments", "lending", "crypto", "p2p", "banking", "wealth", "insurance"],
    "Money Transmission": ["payments", "crypto", "p2p"],
    "Lending": ["lending"],
}


# ─── Change Models ───────────────────────────────────────────────────────────

class RegulatoryChangeNotification:
    """A notification about a regulatory change relevant to a fintech."""

    def __init__(
        self,
        title: str,
        agency: str,
        change_type: str,
        summary: str,
        affected_types: list[str],
        severity: str = "info",
        effective_date: Optional[str] = None,
        source_url: Optional[str] = None,
    ):
        self.title = title
        self.agency = agency
        self.change_type = change_type  # 'new', 'updated', 'amended', 'repealed'
        self.summary = summary
        self.affected_types = affected_types
        self.severity = severity  # 'critical', 'warning', 'info'
        self.effective_date = effective_date
        self.source_url = source_url
        self.timestamp = datetime.utcnow().isoformat()

    def to_dict(self) -> dict:
        return {
            "title": self.title,
            "agency": self.agency,
            "change_type": self.change_type,
            "summary": self.summary,
            "affected_types": self.affected_types,
            "severity": self.severity,
            "effective_date": self.effective_date,
            "source_url": self.source_url,
            "timestamp": self.timestamp,
        }


# ─── Notification Builder ────────────────────────────────────────────────────


def get_recent_changes(
    hours: int = 24,
    agency: Optional[str] = None,
) -> list[dict]:
    """Get recent regulatory changes from the database."""
    conn = get_db()
    since = (datetime.utcnow() - timedelta(hours=hours)).isoformat()

    query = """SELECT * FROM regulatory_changes
               WHERE detected_at >= ?"""
    params: list = [since]

    if agency:
        query += " AND regulation_id IN (SELECT id FROM regulations WHERE agency LIKE ?)"
        params.append(f"%{agency}%")

    query += " ORDER BY detected_at DESC"
    rows = conn.execute(query, params).fetchall()
    conn.close()
    return [dict(r) for r in rows]


def get_latest_regulations_changes(days: int = 7) -> list[dict]:
    """Get regulations added in the last X days."""
    conn = get_db()
    since = (datetime.utcnow() - timedelta(days=days)).isoformat()
    rows = conn.execute(
        """SELECT * FROM regulations
           WHERE ingested_at >= ?
           ORDER BY ingested_at DESC""",
        (since,),
    ).fetchall()
    conn.close()
    return [dict(r) for r in rows]


# ─── Report Generators ───────────────────────────────────────────────────────


def generate_change_report(
    fintech_type: Optional[str] = None,
    days: int = 7,
) -> list[dict]:
    """Generate a change report, optionally filtered by fintech type."""
    changes = get_latest_regulations_changes(days)
    notifications = []

    for change in changes:
        # Determine affected fintech types based on compliance type
        affected = []
        for category, types in TYPES_BY_CATEGORY.items():
            ctype = change.get("compliance_type", "")
            if ctype in category.lower() or category.lower() in ctype.lower():
                affected.extend(types)

        if fintech_type and fintech_type not in affected:
            continue

        severity = "info"
        if change.get("compliance_type") in ("aml", "money_transmission"):
            severity = "critical"
        elif change.get("compliance_type") in ("consumer_protection", "securities"):
            severity = "warning"

        notif = RegulatoryChangeNotification(
            title=change.get("title", "Regulatory Update"),
            agency=change.get("agency", "Unknown"),
            change_type="new" if change.get("ingested_at") else "updated",
            summary=change.get("summary", "")[:500],
            affected_types=list(set(affected)),
            severity=severity,
            effective_date=change.get("effective_date"),
            source_url=change.get("source_url"),
        )
        notifications.append(notif.to_dict())

    return notifications


def generate_report_by_fintech_type(
    fintech_type: str, days: int = 7
) -> list[dict]:
    """Generate a change report specifically for one fintech type."""
    return generate_change_report(fintech_type=fintech_type, days=days)


# ─── Email / Message Formatters ──────────────────────────────────────────────


def format_report_markdown(notifications: list[dict], title: str = "Regulatory Change Report") -> str:
    """Format change notifications as a Markdown report."""
    if not notifications:
        return f"# {title}\n\n✅ No regulatory changes detected in the reporting period."

    lines = [
        f"# {title}",
        f"",
        f"**Report generated:** {datetime.utcnow().strftime('%B %d, %Y at %H:%M UTC')}",
        f"**Changes found:** {len(notifications)}",
        f"",
    ]

    # Group by severity
    severity_order = {"critical": "🔴 Critical", "warning": "🟡 Warning", "info": "ℹ️ Info"}
    for sev, label in severity_order.items():
        sev_changes = [n for n in notifications if n.get("severity") == sev]
        if not sev_changes:
            continue

        lines.append(f"## {label}")
        lines.append(f"")

        for change in sev_changes:
            lines.append(f"### {change['title']}")
            lines.append(f"")
            lines.append(f"- **Agency:** {change['agency']}")
            lines.append(f"- **Type:** {change['change_type']}")
            lines.append(f"- **Effective:** {change.get('effective_date', 'N/A')}")

            if change.get("summary"):
                lines.append(f"- **Summary:** {change['summary'][:300]}")

            affected = change.get("affected_types", [])
            if affected:
                lines.append(f"- **Affects:** {', '.join(affected)}")

            if change.get("source_url"):
                lines.append(f"- **Source:** {change['source_url']}")

            lines.append(f"")

    return "\n".join(lines)


def format_report_html(notifications: list[dict]) -> str:
    """Format change notifications as HTML."""
    items_html = ""
    for n in notifications:
        sev_class = n.get("severity", "info")
        items_html += f"""
        <div class="change-item {sev_class}">
            <h4>{n['title']}</h4>
            <div class="meta">
                <span class="agency">{n['agency']}</span>
                <span class="type">{n['change_type']}</span>
                <span class="eff-date">{n.get('effective_date', 'N/A')}</span>
            </div>
            <p>{n.get('summary', '')[:300]}</p>
            <div class="tags">{' '.join(f'<span class="tag">{t}</span>' for t in n.get('affected_types', []))}</div>
        </div>"""

    return f"""<!DOCTYPE html>
<html><head><meta charset="utf-8"><title>Regulatory Change Report</title>
<style>
  body {{ font-family: -apple-system, sans-serif; max-width: 700px; margin: 2rem auto; color: #1a1a2e; }}
  h1 {{ color: #16213e; }}
  .change-item {{ border-left: 4px solid #22c55e; padding: 1rem; margin: 1rem 0; background: #f9fafb; border-radius: 4px; }}
  .change-item.critical {{ border-left-color: #dc2626; }}
  .change-item.warning {{ border-left-color: #ea580c; }}
  .meta {{ font-size: 0.85rem; color: #666; margin: 0.5rem 0; }}
  .meta span {{ margin-right: 1rem; }}
  .tag {{ display: inline-block; background: #e5e7eb; padding: 0.1rem 0.5rem; border-radius: 999px; font-size: 0.75rem; margin: 0.15rem; }}
</style></head><body>
<h1>📋 Regulatory Change Report</h1>
<p>{datetime.utcnow().strftime('%B %d, %Y')} — {len(notifications)} changes detected</p>
{items_html}
<p style="color: #9ca3af; font-size: 0.85rem;">Generated by complyAI</p>
</body></html>"""


# ─── CLI ──────────────────────────────────────────────────────────────────────


if __name__ == "__main__":
    import json

    print("📋 Recent Regulatory Changes")
    print("=" * 60)

    for ftype in ["payments", "lending", "crypto"]:
        notifications = generate_report_by_fintech_type(ftype, days=30)
        print(f"\n{ftype.upper()}: {len(notifications)} changes")
        for n in notifications[:3]:
            print(f"  [{n['severity']}] {n['title'][:60]}...")

    # Full report
    print("\n\n--- Full Report ---")
    all_changes = generate_change_report(days=30)
    print(format_report_markdown(all_changes)[:1000])
