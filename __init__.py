"""BigQuery Metrics AppsFlyer AI Agent.

An AI-powered analytics agent that enables natural language queries for AppsFlyer performance 
marketing data stored in Google BigQuery. This system converts plain English questions into 
safe, optimized SQL queries, executes them, and computes standardized growth & monetization 
metrics including installs, ROAS, retention, revenue cohorts, and cost efficiency.

Key Features:
- Natural Language → SQL conversion with schema awareness
- AppsFlyer-specific marketing & monetization metrics
- Conversational context and follow-up suggestions
- Safety guardrails: SELECT-only, limits, cost estimation
- Multi-agent architecture with specialized expertise
- Pluggable LLM backend support

Architecture:
This package consists of three main components:

1. **AppsFlyer Metrics Sub-Agent** (`appsflyer_metrics_sub_agent`):
   Expert consultant for AppsFlyer metrics definitions, calculations, and best practices.

2. **BigQuery Analyst Sub-Agent** (`bigquery_analyst_sub_agent`):
   Specialized data analyst for executing queries and exploring BigQuery datasets.

3. **Manager Agent** (`mannger_agent`):
   Intelligent orchestrator that coordinates between metrics expertise and data analysis.

Usage:
The system follows a two-step workflow where the manager agent first consults the AppsFlyer
expert for proper metric definitions, then queries the actual data using those specifications.
This ensures that all analytics are both technically accurate and aligned with mobile marketing
best practices.

Example Questions:
- "Compare D7 ROAS for Meta vs Google last month"
- "Show installs and revenue by media source last 7 days"
- "What's my retention rate for July cohorts?"
- "Break down campaign performance by geo and platform"

Think of it as a conversational analyst for your AppsFlyer + BigQuery data.
"""

__version__ = "1.0.0"
__author__ = "BigQuery Metrics AppsFlyer AI Agent Team"
__description__ = "AI-powered analytics agent for AppsFlyer marketing data in BigQuery"

# Import main components for easy access
from mannger_agent import root_agent
from appsflyer_metrics_sub_agent.agent import appsflyer_metrics_agent
from bigquery_analyst_sub_agent.agent import bigquery_analyst_agent

__all__ = [
    "root_agent",
    "appsflyer_metrics_agent", 
    "bigquery_analyst_agent"
]