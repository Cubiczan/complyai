# complyAI — RegTech for Indie FinTechs

**Compliance automation that doesn't cost your runway.**

complyAI is a self-service RegTech assistant built for indie fintechs — the bootstrapped, the pre-seed, the Stripe Atlas founders who need to get compliance right without hiring a $50k/year compliance officer or paying ComplyAdvantage $500+/mo.

## What It Does

- **🔄 Ingest Regulations** — Automatically fetches rules from SEC (EDGAR), FinCEN (BSA/AML), CFPB, and state regulators
- **✅ Generate Checklists** — Tell us what kind of fintech you are (payments, lending, crypto, etc.), get a compliance checklist tailored to your business
- **📝 Generate Documents** — Terms of Service, Privacy Policies, EULAs, and regulatory disclosures with {{variables}} you customize
- **🔔 Monitor Changes** — Track regulatory updates that affect your fintech type, get notified what changed and what you need to do

## Tech Stack

| Layer | Technology |
|-------|-----------|
| **Backend** | Python 3.11+ / FastAPI |
| **Database** | SQLite (dev) → Postgres (prod) |
| **Scraping** | requests + BeautifulSoup4 |
| **Frontend** | Static HTML + Tailwind CSS CDN |
| **Caching** | SQLite-backed (ready for Redis) |

## Quick Start

```bash
# Clone and enter the project
cd products/complyai

# Install dependencies
pip install -r requirements.txt

# Initialize the database
python -c "from engine.ingest import init_db; init_db()"

# Start the API server
uvicorn main:app --reload --port 8000

# Open the landing page
open frontend/index.html
```

## API Endpoints

| Method | Path | Description |
|--------|------|-------------|
| POST | `/api/checklist` | Generate compliance checklist for a fintech type |
| GET | `/api/ingest/{agency}` | Trigger regulatory ingestion from an agency |
| GET | `/api/monitor/changes` | Get recent regulatory changes |
| POST | `/api/templates/generate` | Generate a document from a template |

## Pricing

| Plan | Price | What You Get |
|------|-------|-------------|
| **Compliance** | $49/mo | Checklists + Document Templates |
| **Growth** | $149/mo | Monitoring + Multi-jurisdiction + Priority updates |
| **Enterprise** | Custom | Private instance, custom integrations, SLA |

## Roadmap

- **Phase 1** — Ingestion engine + checklist generator (MVP)
- **Phase 2** — Template engine + change monitoring
- **Phase 3** — Multi-agent AI: auto-fill templates, personalized guidance, cross-jurisdiction mapping

## Why complyAI?

ComplyAdvantage starts at $500/mo. Ascent starts at $1,000+/mo. Both require sales calls, demo meetings, enterprise onboarding.

complyAI is: **Self-service. No sales calls. Real documents. AI-powered but practical.**

Built for the indie fintech — because compliance shouldn't cost more than your cloud bill.

---

*"Compliance is a feature, not a barrier."*
