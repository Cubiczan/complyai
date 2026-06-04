# Business Plan — complyAI

## Problem

Indie fintechs face the same regulatory burden as Stripe or Square, but with 1/1000th of the resources:

- **No compliance team** — a 2-5 person startup can't afford a full-time compliance officer ($120k-$180k/yr)
- **Enterprise RegTech is too expensive** — ComplyAdvantage ($500+/mo), Ascent ($1,000+/mo), OneTrust ($2,000+/mo)
- **Sales-gated** — every enterprise RegTech requires a demo call, procurement process, enterprise onboarding
- **Not built for bootstrappers** — existing tools assume you have legal counsel, compliance budget, and institutional backing
- **Changes are hard to track** — regulations change constantly, and there's no affordable way to monitor what matters

A fintech founder told us: *"I spent three weeks trying to figure out if we needed a money transmitter license. I just needed someone to tell me the answer."*

## Solution

**complyAI** — the self-service RegTech assistant for indie fintechs.

- Tell us what kind of fintech you are → get a compliance checklist in seconds
- Generate ToS, Privacy Policy, EULAs, and disclosures with {{variables}} you customize
- Monitor regulatory changes that affect *your* fintech type
- No sales calls, no procurement, $49/mo

## Market

### RegTech Market Growth

| Metric | Value |
|--------|-------|
| Current market size (2026) | $4.3B |
| Projected market size (2030) | $12.3B |
| CAGR | ~24% |
| Primary drivers | Regulatory complexity increase, fintech growth, AI adoption |

### Target Segment

**Indie fintechs** — companies that are:
- Bootstrapped or pre-seed/seed funded
- 1-20 employees
- Building on Stripe Atlas, Mercury, Airwallex, etc.
- Operating in payments, lending, crypto, P2P, banking, wealth, or insurance
- US-focused (initially) with eventual multi-jurisdiction needs

**Estimated TAM:** ~50,000 fintech companies globally, ~20,000 US-based. At $49/mo average revenue per user (ARPU): **$11.7M/yr addressable ARR**.

### Existing Solutions Gap

| Solution | Starting Price | Self-Service? | Real Docs? | Indie-Friendly? |
|----------|---------------|---------------|------------|-----------------|
| ComplyAdvantage | $500/mo | ❌ | ❌ (checklists only) | ❌ |
| Ascent | $1,000+/mo | ❌ | ❌ | ❌ |
| OneTrust | $2,000+/mo | ❌ | ❌ | ❌ |
| **complyAI** | **$49/mo** | **✅** | **✅** | **✅** |

## Unit Economics

| Metric | Compliance ($49) | Growth ($149) |
|--------|-----------------|---------------|
| Monthly revenue | $49 | $149 |
| Annual revenue | $588 | $1,788 |
| Gross margin target | 70% | 75% |
| Cost to serve | ~$15/mo | ~$37/mo |
| CAC target | < $200 | < $200 |
| LTV (24mo avg retention) | $1,411 | $4,291 |
| LTV:CAC ratio | 7:1 | 21:1 |

## Differentiation

1. **Price** — 90% less than enterprise RegTech
2. **Self-service** — sign up, pay, go. No demos, no sales calls, no procurement.
3. **Real documents** — not just checklists. Generate ToS, Privacy Policies, EULAs, Reg E/Reg Z disclosures.
4. **AI-powered, not AI-washed** — uses LLMs intelligently: parsing regulations, generating checklists, diff'ing changes
5. **Built for indie fintechs** — we understand what it's like to have 3 people, no lawyers, and a regulatory deadline

## Go-to-Market

See [marketing-plan.md](marketing-plan.md) for details. Summary:

- Indie Hacker communities (Indie Hackers, Hacker News, fintech Discords)
- Stripe Atlas and Mercury integration partnerships
- Content marketing: "regulatory change of the week" newsletter
- Founder-led sales: no sales team, just a good product and word of mouth
- Free tier: basic checklist + 1 document generation (to show value)

## Financial Projections (Conservative)

| Year | Customers | MRR | ARR |
|------|-----------|-----|-----|
| Year 1 | 500 | $24,500 | $294,000 |
| Year 2 | 2,500 | $122,500 | $1.47M |
| Year 3 | 10,000 | $490,000 | $5.88M |

**Assumptions:** 70% on Compliance plan, 30% on Growth plan. 3% monthly churn in Y1, improving to 1.5% by Y3.

## Funding Needs

complyAI can be bootstrapped to profitability:

- **MVP build:** ~$0 (existing tools, open source)
- **Hosting:** ~$100/mo (DigitalOcean/Linode, single box, upgraded as needed)
- **LLM API costs:** ~$200-$500/mo at scale (OpenAI/Claude API for parsing and generation)
- **Monthly burn at launch:** ~$500-$1,000/mo

**Profitability threshold:** ~50-80 customers ($2,450-$3,920/mo MRR).
