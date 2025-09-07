# BigQuery Metrics AppsFlyer AI Agent

An AI-assisted analytics agent that lets you query AppsFlyer performance marketing metrics stored in Google BigQuery using natural language. It translates user questions ("Show installs and ROAS for my top geo last week") into optimized SQL, executes against your curated BigQuery dataset, and returns concise answers, visualizations, and follow‑up insights.

---
## 🚀 Core Features
- **Natural Language to SQL**: Convert plain English questions into safe, parameterized BigQuery SQL.
- **AppsFlyer Marketing Metrics**: Installs, clicks, CVR, retention, revenue, ROAS, cohorts, SKAN (if available), cost metrics (if cost data ingested), and custom events.
- **Schema-Aware Reasoning**: Dynamically inspects information_schema or a local schema manifest to improve query correctness.
- **Result Summarization**: LLM-generated plain‑English explanations of query outputs.
- **Visualization Support**: Returns chart spec suggestions (e.g. JSON for line / bar charts) suitable for frontend rendering.
- **Follow‑Up Memory**: Maintains conversational context ("Compare that to the previous month") across turns.
- **Safety Layer**: Query guardrails (deny DDL/DML, rate limit, row caps, cost estimation, token / quota checks).
- **Extensible Model Backend**: Pluggable providers (OpenAI, Anthropic, Vertex AI, etc.).

---
## 🧩 Architecture Overview
```
User -> API / Chat UI -> Orchestrator -> (1) Intent + SQL Draft (LLM)
                                      -> (2) SQL Validator / Guard
                                      -> (3) BigQuery Runner
                                      -> (4) Result Post-Processor (metrics enrichment, derived KPIs)
                                      -> (5) Insight + Visualization Generator (LLM)
                                      -> Response JSON -> UI Renderer
```
Key modules:
- `agent/intent.py` – prompt construction & conversation state handling
- `agent/sql_generator.py` – NL → SQL synthesis
- `agent/sql_validator.py` – static + rule based safety filters
- `data/bq_client.py` – BigQuery execution + dry-run cost checks
- `agent/insights.py` – summarization & follow‑ups
- `schemas/` – schema manifest or auto‑introspected cache

(Adjust file names to match actual codebase if they differ.)

---
## 📦 Data Model & Metrics
Typical base tables (yours may differ):
- `raw_events` – in‑app events with event_name, event_time, appsflyer_id, media_source, geo, platform
- `installs` – install dimension table (install_time, campaign, adset, channel, geo)
- `attribution_cost` – media cost (media_source, date, cost, currency)
- `revenue_events` – purchase or ad revenue events (value, currency, event_time)
- `skan_installs` – SKAdNetwork postbacks (optional)

Common derived metrics:
- `installs`, `clicks`, `cvr = installs / clicks`
- `day_1_retention`, `day_7_retention`
- `revenue_d{n}` (cohort windows)
- `roas_d{n} = revenue_d{n} / cost`
- `arpu = revenue / active_users`

Add / adjust according to your actual dataset.

---
## 🔐 Prerequisites
1. A Google Cloud project with BigQuery enabled
2. AppsFlyer data exported / ingested into BigQuery (via Data Locker / ETL)
3. Python 3.10+ (or specified runtime)
4. An LLM provider API key (OpenAI / Anthropic / Vertex / etc.)
5. (Optional) Frontend container / Next.js / Streamlit app for chat UI

---
## ⚙️ Environment Variables
Create a `.env` (never commit secrets):
```
GCP_PROJECT_ID=your-gcp-project
BQ_DATASET=marketing_analytics
# If using a service account json path:
GOOGLE_APPLICATION_CREDENTIALS=/path/to/sa.json

# AppsFlyer / data integration
APPSFLYER_APP_ID=yourappID
APPSFLYER_API_TOKEN=xxxxx

# LLM configuration
MODEL_PROVIDER=openai            # openai | anthropic | vertex | azure_openai
MODEL_NAME=gpt-4o-mini           # or claude-3-5-sonnet, etc.
OPENAI_API_KEY=sk-...
ANTHROPIC_API_KEY=...
VERTEX_LOCATION=us-central1
VERTEX_MODEL=projects/xxx/locations/us-central1/models/xxx

# Safety / limits
MAX_ROWS=5000
QUERY_TIMEOUT_SECONDS=60
ALLOW_UNSAFE_SQL=false
```

---
## 🛠️ Local Development
1. Clone repo:
   ```bash
   git clone https://github.com/rivka14/bigquery-metrics-appsflyer-ai-agent.git
   cd bigquery-metrics-appsflyer-ai-agent
   ```
2. Create & activate virtual environment:
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # Windows: .venv\Scripts\activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Copy example env & edit:
   ```bash
   cp .env.example .env
   ```
5. Run dev server / CLI (example):
   ```bash
   python -m app.main
   ```

---
## 🧪 Testing
```bash
pytest -q
```
Recommended: include unit tests for
- SQL generation prompt functions
- Safety validator edge cases
- Metrics post-processing correctness

---
## 🗣️ Example Queries
| User Question | Generated Intent | Example SQL Sketch |
|---------------|------------------|--------------------|
| Install and revenue by media source last 7 days | timeseries_comparison | SELECT date, media_source, COUNT(*) installs, SUM(revenue) revenue ... |
| What was D7 ROAS for Facebook campaigns in August? | cohort_roas | (cohort revenue join cost) |
| Compare ROAS this week vs previous week | period_compare | Two CTEs + diff % |
| Top 5 geos by installs yesterday | ranking | ORDER BY installs DESC LIMIT 5 |

---
## 🧠 Prompt / Guardrail Strategy
- System prompt enumerates allowed metrics & tables.
- Few-shot examples for each query archetype (timeseries, ranking, cohort, retention, roas, funnel).
- Post-LMM regex + SQL AST parse (e.g., sqlglot) to confirm only SELECT, no wildcards, row limit enforced.
- Dry‑run BigQuery to estimate bytes; abort if exceeding threshold.

---
## 🪪 Security & Compliance
- Principle of least privilege: service account limited to SELECT on curated dataset.
- Secrets loaded from environment / secret manager, never embedded in prompts.
- Optional: per-user audit log of natural question, SQL, execution stats, cost.
- PII handling: redact user identifiers unless essential.

---
## 🚀 Deployment
Options:
1. Cloud Run (Docker)
2. Vertex AI Model Garden + Functions for serverless orchestration
3. FastAPI / Uvicorn on GCE or managed K8s (GKE)

Example (Cloud Run):
```bash
gcloud builds submit --tag gcr.io/$GCP_PROJECT_ID/af-metrics-agent:$(git rev-parse --short HEAD)
gcloud run deploy af-metrics-agent \
  --image gcr.io/$GCP_PROJECT_ID/af-metrics-agent:$(git rev-parse --short HEAD) \
  --region=us-central1 --platform=managed \
  --allow-unauthenticated
```
Configure env vars in Cloud Run console or use `--set-env-vars`.

---
## 📤 API Response Shape (Example)
```json
{
  "query_id": "2025-09-07T20:45:00Z_fb1a",
  "user_question": "Show installs and revenue by media source last 7 days",
  "generated_sql": "SELECT ... LIMIT 5000",
  "bytes_processed": 12345678,
  "rows": [...],
  "summary": "Meta and Google drove 78% of installs; Meta ROAS higher (+12%).",
  "chart": {
    "type": "line",
    "x": "date",
    "series": ["installs", "revenue"],
    "group": "media_source"
  },
  "follow_up_suggestions": [
    "Break down Meta installs by campaign",
    "Show D7 ROAS instead of revenue",
    "Compare to previous 7 days"
  ]
}
```

---
## 🧭 Roadmap
- [ ] Add semantic layer / metric definitions (dbt or YAML)
- [ ] Add caching layer for repeated queries
- [ ] Add cost anomaly alerts (spend spike detection)
- [ ] Support SKAN conversion value decoding
- [ ] Add RAG over internal analytics documentation
- [ ] Add streaming token responses
- [ ] Add user-level permission / RBAC

---
## 🤝 Contributing
1. Fork the repo & create a feature branch.
2. Write clear commit messages.
3. Add / update tests where appropriate.
4. Open a PR with description, screenshots (if UI), and checklist.

---
## 📄 License
Choose a license (MIT, Apache 2.0, etc.). Example:
```
MIT License – see LICENSE file (to be added).
```

---
## 🙋 Support / Questions
Open an issue or start a discussion. Feel free to suggest new metric templates or safety improvements.

---
## ⭐ Acknowledgements
- AppsFlyer for the marketing analytics ecosystem
- Google BigQuery for scalable analytics
- Open-source LLM / prompt tooling community

---
**Next Step:** Replace placeholders with your actual file/module names & add a LICENSE.