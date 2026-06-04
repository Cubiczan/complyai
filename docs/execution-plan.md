# Execution Plan — complyAI

## Overview

complyAI is built in three phases, starting with the core value proposition and expanding into AI-augmented compliance automation. Each phase is designed to be self-sustaining — you can launch after Phase 1 and iterate.

## Phase 1: MVP — Ingestion + Checklist Generator (Weeks 1-4)

**Goal:** A working product that can take a fintech type and return a compliance checklist.

### Week 1: Foundation
- [x] Set up project structure (engine/, checklist/, templates/, monitor/, docs/)
- [x] Database schema: regulations, checklists, fintech_types, templates
- [x] `engine/ingest.py` — SEC EDGAR ingestion (free API)
- [x] `engine/ingest.py` — CFPB ingestion (cfpb.gov API)
- [x] `engine/ingest.py` — FinCEN scraping (fincen.gov)
- [x] `engine/ingest.py` — State regulator hardcoded summaries
- [x] `engine/parser.py` — Parse HTML/PDF into structured rules

### Week 2: Core Features
- [x] `checklist/types.py` — Fintech type → regulation mapping
- [x] `checklist/generator.py` — Generate compliance checklist from fintech type
- [x] `checklist/output.py` — Render as HTML or Markdown
- [x] `monitor/watcher.py` — Daily check for regulatory updates
- [x] `monitor/diff.py` — Compare old vs new regulation text

### Week 3: Templates + API
- [x] `templates/` — Terms of Service, Privacy Policy, EULA, disclosure templates
- [x] `monitor/notify.py` — Generate change notification report
- [x] `main.py` — FastAPI server with all endpoints
- [x] `requirements.txt` — Dependencies

### Week 4: Frontend + Launch Prep
- [x] Landing page (static HTML + Tailwind CDN)
- [x] Dashboard concept page
- [x] Testing and edge cases
- [x] Documentation (README, business plan, marketing plan, execution plan, unit economics)

### Phase 1 Trade-offs
- ✅ SQLite (not Postgres) — fast iteration, easy backup, upgrade later
- ✅ Static HTML (not Next.js) — deploy anywhere (S3, GitHub Pages, Vercel)
- ✅ Hardcoded state summaries for NY, CA, TX (real parsing later)
- ❌ No auth yet (Phase 2)
- ❌ No payments integration (Phase 2)
- ❌ No multi-user support (Phase 2)

## Phase 2: Production Ready (Weeks 5-10)

**Goal:** A self-serve SaaS that people can sign up for and pay.

### Week 5-6: Auth + Payments
- [ ] User authentication (Magic Link via email, or Google OAuth)
- [ ] Customer.io for email/onboarding (already configured)
- [ ] Stripe integration for subscriptions ($49/mo, $149/mo)
- [ ] Rate limiting per user tier

### Week 7-8: Monitoring + Notifications
- [ ] Automated daily crawls (cron job)
- [ ] Email notifications for regulatory changes
- [ ] "What changed" summaries by fintech type
- [ ] Webhook notifications for power users

### Week 9-10: Polish
- [ ] Real Dashboard (Svelte or simple Vue app)
- [ ] Better onboarding flow
- [ ] User feedback integration
- [ ] Analytics (PostHog or Plausible)

## Phase 3: Multi-Agent AI (Weeks 11-16)

**Goal:** AI agents that can answer compliance questions, fill templates, and map cross-jurisdiction requirements.

### Week 11-12: AI Checklist Enhancement
- [ ] LLM-powered checklist refinement (Claude API)
- [ ] Contextual questions: "How many employees?" → adjusts AML requirements
- [ ] Business model analysis: "Marketplace vs direct lender → different disclosures"

### Week 13-14: AI Document Generation
- [ ] Auto-fill templates from user answers
- [ ] Custom clause generation
- [ ] Cross-jurisdiction mapping: "You're in NY and TX → here's what changes"

### Week 15-16: Compliance Assistant
- [ ] Q&A: "Ask anything about regulation X"
- [ ] Gap analysis: "Here's what you're missing"
- [ ] Priority ranking: "Fix this first, deal with this later"
- [ ] Export to PDF/DOCX

## Long-Term Vision

### Year 1
- 500+ paying customers
- Coverage for all 50 US states
- Multi-jurisdiction support (US + EU + UK)

### Year 2
- API-first: embed compliance into fintech products
- Partnership with Stripe Atlas, Mercury, Airwallex
- 2,500+ paying customers

### Year 3
- Full multi-agent compliance assistant
- SOC 2 compliance for complyAI itself (eat your own dog food)
- Open-source compliance data commons
- 10,000+ paying customers

## Risk Mitigation

| Risk | Mitigation |
|------|-----------|
| Regulation changes break ingestion | Defensive parsing; fallback to manual updates; clear "not legal advice" disclaimers |
| LLM costs eat margin | Caching, batching, tiered model usage (cheap model for checklist, expensive model for documents) |
| Competition from big RegTechs | Different market — they don't want $49 customers. Focus on service and community. |
| Liability concerns | Strong disclaimers, "this is a tool not an attorney" messaging, limit claims to educational value |
| Low conversion from free to paid | Free tier is intentionally limited; show value, then gate depth |
