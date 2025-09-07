# BigQuery Metrics AppsFlyer AI Agent

An AI-powered analytics agent that lets you ask natural language questions about AppsFlyer performance marketing data stored in Google BigQuery. It converts plain English into safe, optimized SQL, executes it, computes standardized growth & monetization metrics (installs, ROAS, retention, revenue cohorts, cost efficiency), and returns structured results with summaries, visualization specs, and suggested follow‑ups.

> Think of it as a conversational analyst for your AppsFlyer + BigQuery data.

---
## Table of Contents
1. Overview
2. Problem & Why It Matters
3. Core Features
4. How It Works (Flow)
5. Architecture
6. Data Model & Metrics
7. Safety & Governance
8. Quick Start
9. Example Questions
10. API Response Shape
11. Roadmap
12. Contributing
13. FAQ
14. License

---
## 1. Overview
Modern growth and marketing teams constantly ask repetitive data questions: "What is D7 ROAS for Meta vs Google?" "Did installs drop week over week?" "Which campaigns drove the retention lift?" Writing & validating SQL each time is slow and costly. This agent removes friction—turning natural questions into governed, validated, and explainable analytics answers.

## 2. Problem & Why It Matters
| Challenge | Pain | Impact |
|-----------|------|--------|
| Ad-hoc SQL for routine metrics | Repetition & errors | Wasted analyst cycles |
| Inconsistent metric formulas | Misaligned decisions | Lost budget efficiency |
| Costly / unbounded warehouse queries | Budget surprises | Reduced trust |
| Slow iteration on hypotheses | Slower optimization | Lower ROAS / growth |
| Non-technical stakeholders blocked | Backlogs | Delayed insights |

This project standardizes access, enforces safe patterns, and accelerates decision-making.

## 3. Core Features
- Natural Language → SQL (schema-aware, parameterized, SELECT-only)
- AppsFlyer marketing & monetization metrics (installs, cost, revenue, ROAS, retention, cohorts)
- Conversational context ("compare to last month", "break that down by geo")
- Guardrails: no DDL/DML, enforced LIMIT, byte-scan estimation, allowlists
- Post-query insight summarization & suggested follow-ups
- Visualization spec generation (chart-friendly JSON)
- Pluggable LLM backend (OpenAI / Anthropic / Vertex / Azure)
- Extensible metric registry & schema manifest

## 4. How It Works (Flow)
1. User asks: "Compare D7 ROAS for Meta vs Google last month."  
2. Intent classification (period_compare + roas_cohort)  
3. Schema context loaded (table + column manifest)  
4. LLM drafts SQL (safe template-driven)  
5. Validation: static rules + SQL parsing + dry-run cost  
6. BigQuery execution (SELECT-only)  
7. KPI enrichment (ROAS deltas, rankings)  
8. Summarization (plain-English narrative)  
9. Visualization spec assembly  
10. Response JSON with follow-up suggestions

## 5. Architecture
```
User -> Chat/API -> Orchestrator
  -> Intent + SQL Draft (LLM)
  -> SQL Validator (rules + AST + cost dry-run)
  -> BigQuery Runner
  -> Metrics Post-Processor
  -> Insight & Visualization Generator (LLM)
  -> JSON Response -> UI
```
Key conceptual modules (adjust to actual code names):
- intent.py – conversation state & intent classification
- sql_generator.py – NL → SQL templates
- sql_validator.py – guardrails & AST safety checks
- bq_client.py – execution + dry run cost
- insights.py – summarization, suggestions
- schemas/ – manifest or auto-introspect cache

## 6. Data Model & Metrics
Typical tables (customize to your dataset):
- installs (install_time, media_source, geo, campaign, platform)
- attribution_cost (date, media_source, cost, currency)
- revenue_events (event_time, value, currency, type)
- raw_events (generic in-app events)
- skan_installs (optional SKAdNetwork postbacks)

Derived metrics:
- installs, clicks, cvr = installs / clicks
- revenue_d{n}, roas_d{n} = revenue_d{n} / cost
- day_n_retention
- arpu = revenue / active_users
- share_of_installs = installs / total_installs

## 7. Safety & Governance
| Guardrail | Description |
|-----------|-------------|
| SELECT-only | Reject DDL/DML (DROP, UPDATE, INSERT, etc.) |
| LIMIT enforcement | Auto-inject configurable LIMIT if missing |
| Wildcard control | Discourage SELECT *; use explicit columns |
| Cost estimation | BigQuery dry run bytes threshold |
| Column allowlist | Avoid leaking PII or unapproved fields |
| Audit log (optional) | Log question, SQL, bytes, latency |
| Metric registry | Single source of truth for formulas |

## 8. Quick Start
Prerequisites: GCP project, BigQuery dataset with AppsFlyer exports, Python 3.10+, LLM API key.

Environment (.env example):
```
GCP_PROJECT_ID=your-gcp-project
BQ_DATASET=marketing_analytics
GOOGLE_APPLICATION_CREDENTIALS=/path/to/service_account.json
MODEL_PROVIDER=openai
MODEL_NAME=gpt-4o-mini
OPENAI_API_KEY=sk-...
MAX_ROWS=5000
QUERY_TIMEOUT_SECONDS=60
ALLOW_UNSAFE_SQL=false
```

Local setup:
```bash
git clone https://github.com/rivka14/bigquery-metrics-appsflyer-ai-agent.git
cd bigquery-metrics-appsflyer-ai-agent
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env  # if provided; else create manually
python -m app.main  # or your entrypoint
```
Testing (adjust if tests exist):
```bash
pytest -q
```

## 9. Example Questions
| Natural Question | Intent Pattern | Notes |
|------------------|---------------|-------|
| Installs and revenue by media source last 7 days | timeseries_comparison | Daily granularity |
| D7 ROAS for Facebook campaigns in August | cohort_roas | Date filter + campaign slice |
| Compare ROAS this week vs previous week | period_compare | Two windows diff |
| Top 5 geos by installs yesterday | ranking | Limit & ordering |
| Show D1 and D7 retention by platform for July installs | retention_cohort | Cohort expansion |

## 10. API Response Shape (Example)
```json
{
  "query_id": "2025-09-07T20:45:00Z_fb1a",
  "user_question": "Show installs and revenue by media source last 7 days",
  "generated_sql": "SELECT ... LIMIT 5000",
  "bytes_processed": 12345678,
  "rows": [ {"date":"2025-09-01","media_source":"meta","installs":1234,"revenue":456.78} ],
  "summary": "Meta and Google drove 78% of installs; Meta ROAS higher (+12%).",
  "chart": { "type": "line", "x": "date", "group": "media_source", "series": ["installs","revenue"] },
  "follow_up_suggestions": [
    "Break down Meta installs by campaign",
    "Show D7 ROAS instead of revenue",
    "Compare to previous 7 days"
  ]
}
```

## 11. Roadmap
- [ ] Semantic metric layer (dbt metrics / YAML registry)
- [ ] Query result caching & materialized aggregates
- [ ] Spend anomaly detection alerts
- [ ] SKAN conversion value decoding support
- [ ] RAG over internal documentation / naming conventions
- [ ] Slack / Teams bot integration
- [ ] Role-based metric access (RBAC)
- [ ] Streaming partial responses

## 12. Contributing
1. Fork & create feature branch
2. Add or update tests
3. Ensure linting / formatting passes
4. Open PR with clear description & screenshots (if UI)

## 13. FAQ
Q: Why not just use a BI dashboard?  
A: Dashboards are great for predefined views; this agent shines for fast exploratory and comparative questions without manual SQL.

Q: How do you prevent runaway costs?  
A: Dry-run byte scan thresholds + enforced LIMIT + optional caching.

Q: Can I swap the LLM provider?  
A: Yes—abstracted provider interface; set MODEL_PROVIDER + MODEL_NAME.

Q: How are metrics standardized?  
A: (Planned) Central metric registry / semantic layer ensures formula consistency.

Q: Does it support SKAN?  
A: Yes, if you provide a skan_installs-like table; logic can extend to incremental postback decoding.

## 14. License
(Choose a license—MIT, Apache 2.0, etc.)

---
### Next Steps / TODO After Cloning
- Replace placeholder module names with actual file paths
- Add a LICENSE file
- Create tests for SQL guardrails & metric computations
- Add a schema manifest example (schemas/manifest.yaml)

---
Feel free to request a lighter business-friendly summary or a diagram (Mermaid) and I can add it here.