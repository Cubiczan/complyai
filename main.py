"""
main.py — FastAPI server for complyAI.

Endpoints:
  POST /api/checklist          — Generate compliance checklist for fintech type
  GET  /api/ingest/{agency}    — Trigger regulatory ingestion
  GET  /api/monitor/changes    — Get recent regulatory changes
  POST /api/templates/generate — Generate document from template

Run: uvicorn main:app --reload --port 8000
"""

import json
import logging
from datetime import datetime, timedelta
from pathlib import Path
from typing import Optional

from fastapi import Depends, FastAPI, HTTPException, Query
from pydantic import BaseModel, Field

from cubiczan_resilience import require_auth, cors_allowlist

# Enable relative imports for direct module usage
import sys
sys.path.insert(0, str(Path(__file__).parent))

from engine.ingest import (
    ingest_all,
    ingest_sec,
    ingest_fincen,
    ingest_cfpb,
    ingest_state_regulators,
    get_regulations,
    init_db,
)
from engine.crawler import crawl_all, detect_changes
from checklist.generator import generate_checklist, checklist_to_dict
from checklist.output import to_markdown, to_html as checklist_to_html
from templates import (
    get_available_templates,
    render_template,
    list_template_variables,
    TEMPLATE_METADATA,
)
from monitor.notify import (
    generate_change_report,
    generate_report_by_fintech_type,
    RegulatoryChangeNotification,
)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("complyai")

app = FastAPI(
    title="complyAI API",
    description="RegTech Assistant for indie fintechs — compliance checklists, document templates, and regulatory monitoring",
    version="1.0.0",
)

# Replace wildcard CORS with an explicit allowlist (fail-closed; configurable
# via the COMPLYAI_CORS_ORIGINS env var, comma-separated).
cors_allowlist(
    app,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ─── Startup ─────────────────────────────────────────────────────────────────

@app.on_event("startup")
async def startup():
    """Initialize database on startup."""
    init_db()
    logger.info("✅ complyAI database initialized")
    logger.info(f"   DB: {Path(__file__).parent / 'complyai.db'}")


# ─── Request/Response Models ────────────────────────────────────────────────

class ChecklistRequest(BaseModel):
    fintech_type: str = Field(..., description="Type of fintech (payments, lending, crypto, p2p, banking, wealth, insurance)")
    jurisdiction: str = Field("US", description="Jurisdiction")
    format: str = Field("json", description="Output format: json, markdown, or html")
    min_priority: int = Field(10, description="Minimum priority level to include (1=critical, 10=all)")

class ChecklistResponse(BaseModel):
    fintech_type: str
    display_name: str
    generated_at: str
    jurisdiction: str
    summary: dict
    items: list[dict]

class TemplateRequest(BaseModel):
    slug: str = Field(..., description="Template identifier")
    variables: dict[str, str] = Field(default_factory=dict, description="Variable values to fill in")
    fintech_type: Optional[str] = Field(None, description="Optional fintech type filter")

class TemplateResponse(BaseModel):
    slug: str
    name: str
    rendered: str
    variables_used: list[str]
    variables_provided: list[str]

class IngestResponse(BaseModel):
    agency: str
    status: str
    rules_ingested: int
    message: str

class ChangeResponse(BaseModel):
    changes: list[dict]
    count: int
    period_days: int


# ─── API Endpoints ───────────────────────────────────────────────────────────

@app.get("/")
async def root():
    """API root — health check and basic info."""
    return {
        "app": "complyAI",
        "version": "1.0.0",
        "status": "running",
        "endpoints": {
            "POST /api/checklist": "Generate compliance checklist",
            "GET /api/ingest/{agency}": "Trigger regulatory ingestion",
            "GET /api/monitor/changes": "Get recent regulatory changes",
            "POST /api/templates/generate": "Generate document from template",
            "GET /api/templates": "List available templates",
        },
    }


@app.post("/api/checklist", response_model=dict)
async def api_checklist(request: ChecklistRequest):
    """Generate a compliance checklist for a fintech type."""
    logger.info(f"📋 Checklist requested: {request.fintech_type} ({request.format})")

    checklist = generate_checklist(
        fintech_type=request.fintech_type,
        jurisdiction=request.jurisdiction,
        min_priority=request.min_priority,
    )

    if not checklist:
        raise HTTPException(
            status_code=404,
            detail=f"Unknown fintech type: '{request.fintech_type}'. "
                   f"Supported types: payments, lending, crypto, p2p, banking, wealth, insurance",
        )

    if request.format == "markdown":
        from checklist.output import to_markdown
        return {"format": "markdown", "content": to_markdown(checklist)}

    if request.format == "html":
        from checklist.output import to_html
        return {"format": "html", "content": to_html(checklist)}

    # Default: JSON
    return checklist_to_dict(checklist)


@app.get("/api/checklist/supported-types")
async def api_supported_types():
    """List supported fintech types."""
    from checklist.types import FINTECH_TYPES
    return {
        "types": [
            {
                "slug": slug,
                "name": info["display_name"],
                "description": info.get("description", ""),
                "examples": info.get("examples", []),
            }
            for slug, info in FINTECH_TYPES.items()
        ]
    }


@app.get("/api/ingest/{agency}", response_model=IngestResponse)
async def api_ingest(agency: str, _auth=Depends(require_auth)):
    """Trigger regulatory ingestion for a specific agency or 'all'.

    Auth-protected (fail-closed): this triggers outbound crawls and DB writes.
    """
    agency = agency.lower()
    logger.info(f"📥 Ingestion requested: {agency}")

    agency_map = {
        "sec": ("SEC", ingest_sec),
        "fincen": ("FinCEN", ingest_fincen),
        "cfpb": ("CFPB", ingest_cfpb),
        "states": ("State Regulators", ingest_state_regulators),
    }

    if agency == "all":
        results = ingest_all()
        total = sum(results.values())
        return IngestResponse(
            agency="All Agencies",
            status="success",
            rules_ingested=total,
            message=f"Ingested {total} regulations across {len(results)} agencies: {results}",
        )

    if agency not in agency_map:
        raise HTTPException(
            status_code=400,
            detail=f"Unknown agency: '{agency}'. Supported: sec, fincen, cfpb, states, all",
        )

    name, fn = agency_map[agency]
    count = fn()

    return IngestResponse(
        agency=name,
        status="success" if count >= 0 else "partial",
        rules_ingested=count,
        message=f"Ingested {count} regulations from {name}",
    )


@app.get("/api/monitor/changes", response_model=ChangeResponse)
async def api_monitor_changes(
    fintech_type: Optional[str] = Query(None, description="Filter by fintech type"),
    days: int = Query(7, description="Lookback period in days"),
):
    """Get recent regulatory changes, optionally filtered by fintech type."""
    logger.info(f"🔔 Changes requested: fintech_type={fintech_type}, days={days}")

    if fintech_type:
        notifications = generate_report_by_fintech_type(fintech_type, days=days)
    else:
        notifications = generate_change_report(days=days)

    return ChangeResponse(
        changes=notifications,
        count=len(notifications),
        period_days=days,
    )


@app.get("/api/monitor/crawl")
async def api_crawl(_auth=Depends(require_auth)):
    """Trigger a full regulatory crawl across all sources.

    Auth-protected (fail-closed): this triggers outbound crawls and DB writes.
    """
    logger.info("🕷️ Crawl requested")
    results = crawl_all(force=False)
    changes = detect_changes()
    return {
        "status": "ok",
        "results": {
            source: count for source, count in results.items()
        },
        "changes_detected": len(changes),
        "changes": changes[:20],
    }


@app.post("/api/templates/generate", response_model=TemplateResponse)
async def api_template_generate(request: TemplateRequest):
    """Generate a document from a template with variable substitution."""
    logger.info(f"📝 Template requested: {request.slug}")

    # Check template exists
    if request.slug not in TEMPLATE_METADATA:
        available = get_available_templates()
        raise HTTPException(
            status_code=404,
            detail=f"Template '{request.slug}' not found. Available: {[t['slug'] for t in available]}",
        )

    # Render
    rendered = render_template(
        slug=request.slug,
        variables=request.variables,
        fintech_type=request.fintech_type,
    )

    if not rendered:
        raise HTTPException(
            status_code=400,
            detail=f"Template '{request.slug}' is not applicable for fintech type '{request.fintech_type}'",
        )

    # Track which variables were used vs provided
    all_vars = list_template_variables(request.slug)
    provided = [v for v in request.variables if v in all_vars]
    missing = [v for v in all_vars if v not in request.variables]

    return TemplateResponse(
        slug=request.slug,
        name=TEMPLATE_METADATA[request.slug]["name"],
        rendered=rendered,
        variables_used=all_vars,
        variables_provided=provided + missing,  # show defaults for missing
    )


@app.get("/api/templates")
async def api_list_templates(
    fintech_type: Optional[str] = Query(None, description="Filter by fintech type"),
):
    """List available document templates."""
    templates = get_available_templates(fintech_type)
    return {
        "templates": templates,
        "count": len(templates),
    }


@app.get("/api/templates/{slug}")
async def api_template_detail(slug: str):
    """Get template details including variables."""
    if slug not in TEMPLATE_METADATA:
        raise HTTPException(status_code=404, detail=f"Template '{slug}' not found")

    meta = TEMPLATE_METADATA[slug]
    variables = list_template_variables(slug)

    return {
        "slug": slug,
        "name": meta["name"],
        "description": meta["description"],
        "applicable_types": meta["applicable_types"],
        "jurisdiction": meta["jurisdiction"],
        "variables": variables,
        "variable_count": len(variables),
    }


@app.get("/api/db/stats")
async def api_db_stats():
    """Get database statistics."""
    from engine.ingest import get_db
    conn = get_db()

    stats = {}
    for table in ["regulations", "fintech_types", "templates", "regulatory_changes", "crawl_log"]:
        try:
            row = conn.execute(f"SELECT COUNT(*) as c FROM {table}").fetchone()
            stats[table] = row["c"] if row else 0
        except Exception:
            stats[table] = 0

    # Agency breakdown
    agencies = conn.execute(
        """SELECT agency, COUNT(*) as c FROM regulations
           GROUP BY agency ORDER BY c DESC"""
    ).fetchall()
    stats["by_agency"] = {r["agency"]: r["c"] for r in agencies}

    conn.close()
    return {"status": "ok", "stats": stats}


# ─── Run Directly ────────────────────────────────────────────────────────────

if __name__ == "__main__":
    import uvicorn
    print("🚀 Starting complyAI API server...")
    init_db()
    uvicorn.run(app, host="0.0.0.0", port=8000)
