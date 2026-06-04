# Unit Economics — complyAI

## Pricing Tiers

| Feature | Compliance ($49/mo) | Growth ($149/mo) | Enterprise (Custom) |
|---------|-------------------|-------------------|--------------------|
| Compliance checklists | ✅ 5/mo | ✅ Unlimited | ✅ Unlimited |
| Document templates | ✅ 3/mo | ✅ 15/mo | ✅ Unlimited |
| Reg change monitoring | ❌ | ✅ Multi-jurisdiction | ✅ All jurisdictions |
| Email notifications | ❌ | ✅ | ✅ + Slack/Webhook |
| Priority support | ❌ | ✅ (48h) | ✅ (24h SLA) |
| Custom templates | ❌ | ❌ | ✅ |
| Private instance | ❌ | ❌ | ✅ |
| Multi-user | ❌ | ✅ (up to 5) | ✅ (unlimited) |

## Unit Economics per Plan

### Compliance Plan ($49/mo)

| Metric | Value | Notes |
|--------|-------|-------|
| **Revenue** | | |
| Monthly price | $49.00 | |
| Annual (paid upfront, 2mo free) | $49.00 × 10mo | $490/yr effective |
| **Cost to serve** | | |
| LLM API costs | $4.50/mo | ~90 checklists at $0.05 each (Claude Haiku caching) |
| Template generation (3/mo) | $1.50/mo | ~$0.50 per full document generation |
| Monitoring (none on this tier) | $0.00 | |
| Hosting & infra (share) | $3.00/mo | Assuming 500 users per $100/mo server |
| Email/support | $2.00/mo | Customer.io / iteration |
| Stripe fees (2.9% + $0.30) | $1.72/mo | |
| **Gross margin** | | |
| Gross profit per customer | $36.28/mo | |
| Gross margin | **74%** | |
| **Acquisition** | | |
| Target CAC | < $200 | Organic/content-led, very low cost |
| Typical CAC (content marketing) | $15-$50 | Almost entirely organic through communities and SEO |
| **Retention** | | |
| Target monthly churn | 3% | 24-month avg lifetime |
| LTV (24mo avg) | **$870** | At effective ~$36.28/mo gross margin |
| LTV:CAC ratio | **17:1** | At $50 CAC / $870 LTV |

### Growth Plan ($149/mo)

| Metric | Value |
|--------|-------|
| **Revenue** | |
| Monthly price | $149.00 |
| **Cost to serve** | |
| LLM API costs | $22.50/mo (unlimited checklists + monitoring) |
| Monitoring & notifications | $5.00/mo (daily crawls + diff computation) |
| Template generation (15/mo) | $7.50/mo |
| Hosting & infra (share) | $5.00/mo |
| Email/support | $5.00/mo |
| Stripe fees (2.9% + $0.30) | $4.62/mo |
| **Gross margin** | |
| Gross profit per customer | $99.38/mo |
| Gross margin | **67%** |
| **Acquisition** | |
| Target CAC | < $300 (more targeted ads/partnerships) |
| **Retention** | |
| Target monthly churn | 1.5% (stickier product with monitoring) |
| LTV (36mo avg) | **$4,990** |
| LTV:CAC ratio | **17:1** |

### Blended Unit Economics (70% Compliance / 30% Growth)

| Metric | Value |
|--------|-------|
| Blended ARPU | $79.00/mo |
| Blended gross margin | ~72% |
| Blended gross profit | $56.90/mo |
| Target blended CAC | $225 |
| Blended LTV (28mo avg) | $1,593 |
| Blended LTV:CAC | **7:1** |

## Cost Structure (Monthly, at 500 Customers)

| Cost Item | Amount | % of Revenue |
|-----------|--------|-------------|
| LLM API | $5,775 | 14.6% |
| Hosting (DigitalOcean Droplet) | $100 | 0.3% |
| Email/SaaS tools | $500 | 1.3% |
| Stripe fees | $1,958 | 5.0% |
| **Total COGS** | **$8,333** | **21.1%** |
| Gross profit | $31,167 | 78.9% |
| G&A / Founder salary | $6,000 | 15.2% |
| Marketing spend | $1,500 | 3.8% |
| **Net profit** | **$23,667** | **59.9%** |

**Assumptions:** 350 Compliance × $49 + 150 Growth × $149 = $39,500/mo MRR.

## Path to Profitability

| Customers | MRR | Monthly Costs | Profit/(Loss) |
|-----------|-----|---------------|--------------|
| 0 | $0 | $1,000 | ($1,000) |
| 25 | $1,975 | $1,500 | $475 |
| 50 | $3,950 | $1,800 | $2,150 |
| 100 | $7,900 | $2,500 | $5,400 |
| 200 | $15,800 | $4,000 | $11,800 |
| 500 | $39,500 | $12,833 | $26,667 |

**Breakeven: ~15-20 customers** — very achievable for a bootstrapped product.

## Sensitivity Analysis

| Scenario | MRR at 500 customers | Gross Margin | Notes |
|----------|---------------------|--------------|-------|
| Base case | $39,500 | 72% | 70/30 split, moderate LLM costs |
| Bad case — more Growth users | $31,100 | 67% | Switches to 50/50 split, higher cost to serve |
| Good case — more Compliance users | $46,500 | 74% | 80/20 split, mostly checklists |
| Optimistic — higher ARPU | $55,000 | 76% | Add-ons, usage-based pricing |
| Pessimistic — high churn | $12,000 | 50% | 8% monthly churn, lower retention |

## Key Takeaways

1. **complyAI is profitable from ~20 customers** — extremely capital-efficient
2. **CAC is near-zero with content marketing** — no paid spend needed to validate
3. **LTV:CAC > 7:1** even in pessimistic scenarios — healthy unit economics
4. **70%+ gross margins** — scalable with low touch support
5. **LLM API costs are the main variable** — caching and batched processing keep this in check
