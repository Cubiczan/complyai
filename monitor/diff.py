"""
monitor/diff.py — Compare old vs new regulation text and highlight changes.

Uses difflib to generate structured diffs between versions of regulatory
text. Useful for detecting when regulations change.
"""

import difflib
import re
from typing import Optional
from pathlib import Path


# ─── Diff Formatting ─────────────────────────────────────────────────────────

class RegulationDiff:
    """Structured diff between old and new regulation text."""

    def __init__(
        self,
        title: str,
        old_text: str = "",
        new_text: str = "",
        old_hash: Optional[str] = None,
        new_hash: Optional[str] = None,
    ):
        self.title = title
        self.old_text = old_text
        self.new_text = new_text
        self.old_hash = old_hash
        self.new_hash = new_hash
        self._diff = None

    def compute(self) -> list[str]:
        """Compute the diff as unified diff lines."""
        old_lines = self.old_text.splitlines(keepends=True)
        new_lines = self.new_text.splitlines(keepends=True)
        self._diff = list(
            difflib.unified_diff(
                old_lines,
                new_lines,
                fromfile="previous",
                tofile="current",
                n=3,  # context lines
            )
        )
        return self._diff

    def has_changes(self) -> bool:
        """Check if there are meaningful differences."""
        if self._diff is None:
            self.compute()
        # Filter out the header lines
        changes = [l for l in (self._diff or [])
                   if l.startswith("+") or l.startswith("-")]
        return len(changes) > 0

    def summary(self) -> str:
        """Generate a human-readable summary of changes."""
        if self._diff is None:
            self.compute()

        added = sum(1 for l in self._diff if l.startswith("+") and not l.startswith("+++"))
        removed = sum(1 for l in self._diff if l.startswith("-") and not l.startswith("---"))

        if added == 0 and removed == 0:
            return f"No changes for: {self.title}"

        return f"{self.title}: {added} additions, {removed} removals"

    def html_diff(self) -> str:
        """Generate an HTML side-by-side diff view."""
        if self._diff is None:
            self.compute()

        html = ["<div class='regulation-diff'>"]
        html.append(f"<h3>{self.title}</h3>")
        html.append("<table class='diff-table'><tr><th>Previous</th><th>Current</th></tr>")

        old_lines = []
        new_lines = []

        for line in self._diff:
            if line.startswith("---") or line.startswith("+++") or line.startswith("@@"):
                continue
            if line.startswith("+"):
                new_lines.append(f"<span class='added'>{line[1:]}</span>")
            elif line.startswith("-"):
                old_lines.append(f"<span class='removed'>{line[1:]}</span>")
            else:
                old_lines.append(line)
                new_lines.append(line)

        # Pad shorter list
        max_len = max(len(old_lines), len(new_lines))
        old_lines += [""] * (max_len - len(old_lines))
        new_lines += [""] * (max_len - len(new_lines))

        for o, n in zip(old_lines, new_lines):
            html.append(f"<tr><td class='old'>{o}</td><td class='new'>{n}</td></tr>")

        html.append("</table></div>")
        return "\n".join(html)

    def markdown_diff(self) -> str:
        """Generate a Markdown diff for display."""
        if self._diff is None:
            self.compute()

        lines = [f"## Change: {self.title}", ""]
        for line in self._diff:
            if line.startswith("---") or line.startswith("+++"):
                continue
            if line.startswith("@@"):
                lines.append(f"*({line.strip()})*")
                continue
            if line.startswith("+"):
                lines.append(f"```diff\n+ {line[1:].strip()}\n```")
            elif line.startswith("-"):
                lines.append(f"```diff\n- {line[1:].strip()}\n```")
            else:
                lines.append(f"  {line.strip()}")

        lines.append("")
        return "\n".join(lines)

    def json_diff(self) -> dict:
        """Return diff as a JSON-serializable dict."""
        if self._diff is None:
            self.compute()

        changes = []
        for line in self._diff:
            if line.startswith("+"):
                changes.append({"type": "addition", "text": line[1:].strip()})
            elif line.startswith("-"):
                changes.append({"type": "removal", "text": line[1:].strip()})

        return {
            "title": self.title,
            "old_hash": self.old_hash,
            "new_hash": self.new_hash,
            "has_changes": self.has_changes(),
            "changes": changes,
            "summary": self.summary(),
        }


# ─── Convenience Functions ───────────────────────────────────────────────────


def diff_regulation(
    old_text: str,
    new_text: str,
    title: str = "Regulation Change",
    old_hash: Optional[str] = None,
    new_hash: Optional[str] = None,
) -> RegulationDiff:
    """Create and compute a diff for a regulation."""
    diff = RegulationDiff(
        title=title,
        old_text=old_text,
        new_text=new_text,
        old_hash=old_hash,
        new_hash=new_hash,
    )
    diff.compute()
    return diff


def compare_versions(
    old_content: str,
    new_content: str,
    identifier: str,
) -> Optional[RegulationDiff]:
    """Compare two versions of a document and return diff if changed."""
    diff = diff_regulation(old_content, new_content, title=identifier)
    if diff.has_changes():
        return diff
    return None


# ─── Scraped Content Diffs ───────────────────────────────────────────────────


def diff_regulation_by_key(
    old_text: str | None,
    new_text: str | None,
    key: str,
) -> RegulationDiff:
    """Safely diff two texts, handling None."""
    return diff_regulation(
        old_text or "",
        new_text or "",
        title=key,
    )


def extract_changed_sections(diff: RegulationDiff) -> list[dict]:
    """Extract the specific sections that changed (sentence-level)."""
    if diff._diff is None:
        diff.compute()

    changes = []
    current_section = "General"

    for line in diff._diff:
        if line.startswith("@@") and len(line) > 10:
            # Section header
            current_section = line.strip()

        if line.startswith("+"):
            text = line[1:].strip()
            if text:
                changes.append({
                    "section": current_section,
                    "type": "added",
                    "text": text,
                })
        elif line.startswith("-"):
            text = line[1:].strip()
            if text:
                changes.append({
                    "section": current_section,
                    "type": "removed",
                    "text": text,
                })

    return changes


# ─── CLI / Test ──────────────────────────────────────────────────────────────


if __name__ == "__main__":
    old = """Regulation E Section 1005.6:
The consumer's liability for unauthorized transfers is limited to $50
if reported within two business days of learning of the loss or theft."""

    new = """Regulation E Section 1005.6 (Updated):
The consumer's liability for unauthorized transfers is limited to $50
if reported within two business days. For business days 3-60, liability
increases to $500."""

    diff = diff_regulation(old, new, "Regulation E — 12 CFR 1005.6")
    print("=== Summary ===")
    print(diff.summary())
    print("\n=== Markdown Diff ===")
    print(diff.markdown_diff())
    print("\n=== JSON ===")
    import json
    print(json.dumps(diff.json_diff(), indent=2))
