"""Manager Agent Module.

This module provides the main orchestrator agent that coordinates between AppsFlyer metrics
expertise and BigQuery data analysis. The manager agent follows a mandatory two-step workflow:

1. **AppsFlyer Metrics Consultation**: First consults the AppsFlyer metrics agent to understand
   event/metric definitions, calculation methods, required data fields, and business context.

2. **BigQuery Data Analysis**: Then uses the BigQuery analyst agent to find and query actual
   data based on the AppsFlyer requirements and definitions.

The manager agent ensures that:
- All mobile marketing questions are properly contextualized with AppsFlyer expertise
- Data queries align with official AppsFlyer metric definitions and best practices
- Results combine theoretical knowledge with actual data analysis
- Insights connect AppsFlyer standards with real performance data

This coordination approach provides comprehensive mobile marketing analytics that are both
technically accurate and business-relevant.
"""

from . import agent
from .agent import root_agent
from .agent import appsflyer_metrics_agent
from .agent import bigquery_analyst_agent