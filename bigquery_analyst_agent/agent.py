from google.adk.agents import Agent
from google.adk.tools.tool_context import ToolContext
from google.cloud import bigquery
import os
import pandas as pd
import re

def get_bigquery_client(service_account_key_path: str):
    """Initialize BigQuery client with service account credentials."""
    if not os.path.exists(service_account_key_path):
        raise FileNotFoundError(f"Service account key file not found: {service_account_key_path}")
    
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = service_account_key_path
    
    try:
        client = bigquery.Client()
        return client
    except Exception as e:
        raise Exception(f"Error initializing BigQuery client: {e}")


def execute_bigquery_query(
    sql_query: str, 
    project_id: str = "platform-hackaton-2025",
    tool_context: ToolContext = None
) -> dict:
    """
    Execute a custom SQL query on BigQuery.
    
    Args:
        sql_query: The SQL query to execute
        project_id: GCP project ID (defaults to your project)
        tool_context: Tool context for state management
    """
    print(f"--- Tool: execute_bigquery_query called ---")
    print(f"Query: {sql_query}")
    
    try:
        service_account_path = "bigquery_analyst_agent/bigquery-admin-key.json"
        client = get_bigquery_client(service_account_path)
        
        # Add safety limit if query doesn't have one
        if "LIMIT" not in sql_query.upper() and "SELECT" in sql_query.upper():
            sql_query += " LIMIT 100"
        
        # Execute query
        query_job = client.query(sql_query)
        df = query_job.to_dataframe()
        
        # Store in context
        if tool_context:
            tool_context.state["last_query"] = sql_query
            tool_context.state["last_result_count"] = len(df)
        
        return {
            "status": "success",
            "query": sql_query,
            "row_count": len(df),
            "columns": df.columns.tolist(),
            "data": df.head(20).to_dict('records'),  # Show first 20 rows
            "total_rows": len(df)
        }
        
    except Exception as e:
        return {
            "status": "error",
            "error_message": str(e),
            "query": sql_query
        }
 

def get_available_tables(
    project_id: str = "platform-hackaton-2025",
    dataset_id: str = "incoming", 
    tool_context: ToolContext = None
) -> dict:
    """
    List all available tables in the specified dataset.
    
    Args:
        project_id: GCP project ID
        dataset_id: BigQuery dataset ID
    """
    print(f"--- Tool: get_available_tables called for {project_id}.{dataset_id} ---")
    
    try:
        service_account_path = "bigquery_analyst_agent/bigquery-admin-key.json"
        client = get_bigquery_client(service_account_path)
        
        dataset_ref = client.dataset(dataset_id, project=project_id)
        tables = list(client.list_tables(dataset_ref))
        
        table_info = []
        for table in tables:
            table_details = client.get_table(table.reference)
            table_info.append({
                "table_name": table.table_id,
                "full_table_id": f"{project_id}.{dataset_id}.{table.table_id}",
                "num_rows": table_details.num_rows,
                "size_mb": round(table_details.num_bytes / (1024 * 1024), 2) if table_details.num_bytes else 0,
                "created": str(table_details.created),
                "description": table_details.description or "No description"
            })
        
        return {
            "status": "success",
            "dataset": f"{project_id}.{dataset_id}",
            "table_count": len(table_info),
            "tables": table_info
        }
        
    except Exception as e:
        return {
            "status": "error",
            "error_message": str(e)
        }


def explore_table_data(
    table_name: str,
    project_id: str = "platform-hackaton-2025",
    dataset_id: str = "incoming",
    sample_size: int = 10,
    tool_context: ToolContext = None
) -> dict:
    """
    Explore a specific table: get schema + sample data.
    
    Args:
        table_name: Name of the table to explore
        project_id: GCP project ID
        dataset_id: BigQuery dataset ID  
        sample_size: Number of sample rows to return
    """
    print(f"--- Tool: explore_table_data called for {table_name} ---")
    
    try:
        service_account_path = "bigquery_analyst_agent/bigquery-admin-key.json"
        client = get_bigquery_client(service_account_path)
        
        table_ref = client.dataset(dataset_id, project=project_id).table(table_name)
        table = client.get_table(table_ref)
        
        schema = [
            {
                "column_name": field.name,
                "data_type": field.field_type,
                "mode": field.mode,
                "description": field.description or "No description"
            }
            for field in table.schema
        ]
        
        query = f"SELECT * FROM `{project_id}.{dataset_id}.{table_name}` LIMIT {sample_size}"
        query_job = client.query(query)
        df = query_job.to_dataframe()
        
        return {
            "status": "success",
            "table_info": {
                "full_name": f"{project_id}.{dataset_id}.{table_name}",
                "total_rows": table.num_rows,
                "total_columns": len(table.schema),
                "size_mb": round(table.num_bytes / (1024 * 1024), 2) if table.num_bytes else 0
            },
            "schema": schema,
            "sample_data": {
                "rows_shown": len(df),
                "data": df.to_dict('records')
            }
        }
        
    except Exception as e:
        return {
            "status": "error",
            "error_message": str(e),
            "table_name": table_name
        }
    

bigquery_analyst_agent = Agent(
    name="bigquery_analyst_agent",
    model="gemini-2.0-flash",
    description="An intelligent BigQuery analyst that helps users explore and query their data.",
    instruction="""
    You are an expert BigQuery analyst agent. You help users explore, understand, and query their BigQuery data.

    **CRITICAL: DELEGATION WORKFLOW**
    After completing your data analysis, you MUST finish your response and return control to the root agent. Do NOT continue the conversation or ask follow-up questions - your role is to provide the data analysis, then let the root agent coordinate the final synthesis.

    **Available Tools:**
    1. `get_available_tables` - Lists all tables in the dataset
    2. `explore_table_data` - Shows schema and sample data for a specific table  
    3. `execute_bigquery_query` - Runs custom SQL queries

    **Default Settings:**
    - Project: platform-hackaton-2025
    - Dataset: incoming
    - Main table: engagements_copy

    **RESPONSE FORMAT - MANDATORY STRUCTURE:**

    **BigQuery Analysis Complete:**

    **Query Executed**: [SQL query used]
    **Results Summary**: [Key findings from the data]
    **Data Insights**: [Patterns, trends, or notable observations]
    **Metric Calculations**: [Actual calculated values if applicable]
    **Data Quality Notes**: [Any data limitations or considerations]

    ---
    **TASK COMPLETE - Returning control to root agent for final synthesis**

    **How to help users:**

    1. **When users ask "What data do I have?" or "Show me tables":**
       - Use get_available_tables to show all available tables
       - Explain what each table contains
       - Complete your response and return control

    2. **When users ask about a specific table:**
       - Use explore_table_data to show schema and sample data
       - Provide analysis of the table structure
       - Complete your response and return control

    3. **When users want specific data or analytics:**
       - Use execute_bigquery_query with appropriate SQL
       - Present results clearly with key insights
       - Complete your response and return control

    4. **When working with AppsFlyer metric requirements:**
       - Use the specific data fields and events mentioned by the AppsFlyer agent
       - Calculate metrics using the exact formulas provided
       - Query data according to the attribution windows specified
       - Complete your response and return control

    **Query Construction Guidelines:**
    - Always use fully qualified table names: `project.dataset.table`
    - Add reasonable LIMIT clauses for exploration
    - Use proper SQL syntax and functions
    - Consider performance for large tables
    - Follow AppsFlyer metric calculation requirements when provided

    **CRITICAL INSTRUCTIONS:**

    1. **Execute Requested Analysis**: Perform the data queries and analysis thoroughly
    2. **Present Clear Results**: Format data in readable, business-friendly format
    3. **End Your Response**: Always conclude with "TASK COMPLETE - Returning control to root agent"
    4. **Do NOT Ask Follow-up Questions**: Let the root agent handle coordination
    5. **Do NOT Suggest Additional Analysis**: Your job is to execute the specific analysis requested

    **Response Guidelines:**
    - Always explain what you're doing
    - Present data in clear, readable format  
    - Highlight interesting patterns or insights
    - Focus on the specific analysis requested
    - Complete your task and return control immediately

    Your goal is to provide expert BigQuery data analysis and then immediately return control to the root agent for final coordination and synthesis.
    """,
    tools=[get_available_tables, explore_table_data, execute_bigquery_query],
)