"""BigQuery Analyst Sub-Agent Module.

This module provides a specialized BigQuery data analyst agent that handles:
- Executing SQL queries on Google BigQuery datasets
- Exploring table schemas and sample data
- Analyzing AppsFlyer marketing data stored in BigQuery
- Calculating mobile marketing metrics using proper formulas
- Providing data insights, patterns, and recommendations

The agent includes functions for:
- get_available_tables(): List all available BigQuery tables
- explore_table_data(): Show table schema and sample data
- execute_bigquery_query(): Run custom SQL queries with safety controls

All queries follow safety guidelines with proper limits, qualified table names,
and performance considerations for large datasets.
"""

from . import agent
