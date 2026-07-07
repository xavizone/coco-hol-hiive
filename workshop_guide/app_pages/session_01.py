import streamlit as st
from components import render_session_header, render_prompt, render_explanation, render_technologies_used, render_key_concepts, render_what_you_built

render_session_header(1, "Data Prep", "10:00 - 10:25 AM", "25 min", "Database, schema, warehouse, and 10 marketplace tables loaded from CSV")

render_technologies_used([
    {"name": "Database & Schema", "description": "Snowflake's organizational hierarchy for objects. A database contains schemas, and schemas contain tables, views, and other objects.", "icon": "database"},
    {"name": "CSV File Format", "description": "Snowflake can infer schema and load data directly from CSV files hosted at HTTP URLs using file formats and COPY INTO commands.", "icon": "table_chart"},
    {"name": "Virtual Warehouse", "description": "Snowflake's compute engine. A warehouse provides the CPU and memory to execute queries and load data. Scales independently of storage.", "icon": "memory"},
])


PROMPT_1_1 = """Create the following Snowflake objects for our HIIVE AI workshop:

1. A database called HIIVE_AI
2. A schema called MARKETPLACE_OPS inside that database
3. A stage called DATA in the schema MARKETPLACE_OPS with a directory table and server side encryption
3. A warehouse called HIIVE_WH (size MEDIUM, auto-suspend after 60 seconds, auto-resume enabled)
4. Set the session context to use these objects

Execute all SQL and confirm each object was created."""

render_prompt("Prompt 1.1", "Create Database, Schema & Warehouse", PROMPT_1_1)

render_explanation("What this prompt does", """
Creates the foundational Snowflake objects:

```sql
CREATE DATABASE HIIVE_AI;
CREATE SCHEMA HIIVE_AI.MARKETPLACE_OPS;
CREATE WAREHOUSE HIIVE_WH
  WAREHOUSE_SIZE = 'MEDIUM'
  AUTO_SUSPEND = 60
  AUTO_RESUME = TRUE;

USE DATABASE HIIVE_AI;
USE SCHEMA MARKETPLACE_OPS;
USE WAREHOUSE HIIVE_WH;
```

**Why MEDIUM?** We're loading ~1,460 rows total — even X-SMALL would work. MEDIUM gives us comfortable headroom for the Cortex functions we'll use later. With AUTO_SUSPEND = 60 seconds, it will pause immediately after queries finish, minimizing credit usage.
""")


PROMPT_1_2 = """In HIIVE_AI.MARKETPLACE_OPS, the 10 CSV files have been uploaded to an internal stage called DATA.

For all 10 tables (COMPANIES, SHAREHOLDERS, LISTINGS, TRADE_EXECUTIONS, PRICING_SIGNALS, PLATFORM_ACTIVITY, USER_SESSIONS, COMPLIANCE_REVIEWS, SUPPORT_TICKETS, REGULATORY_FILINGS):

1. Create a file format (CSV with PARSE_HEADER=TRUE, FIELD_OPTIONALLY_ENCLOSED_BY='"')
2. Create the tables with appropriate column types inferred from the data. Ensure to convert the column names to uppercase.
3. Load the data

Use CREATE TABLE with INFER_SCHEMA from a stage and then COPY INTO them. The key requirement is that all 10 tables are created and populated.

Execute all SQL."""

st.markdown("""
**Before running the prompt below, download the 10 CSV files and upload them to the `DATA` stage:**

1. Download all files from [github.com/xavizone/coco-hol-hiive/tree/main/workshop_guide/data](https://github.com/xavizone/coco-hol-hiive/tree/main/workshop_guide/data):
   `companies.csv`, `shareholders.csv`, `listings.csv`, `trade_executions.csv`, `pricing_signals.csv`, `platform_activity.csv`, `user_sessions.csv`, `compliance_reviews.csv`, `support_tickets.csv`, `regulatory_filings.csv`
2. Using Snowsight, use the Horizon Catalog to browse to the `HIIVE_AI.MARKETPLACE_OPS.DATA` stage to upload all 10 files.
3. Then copy the prompt below into Cortex Code and execute.
""")

render_prompt("Prompt 1.2", "Load and Create Tables from CSV", PROMPT_1_2)

render_explanation("What this prompt does", """
Loads all 10 marketplace data tables from CSV files uploaded to the internal stage `DATA`. Cortex Code will use INFER_SCHEMA to detect column types automatically:

```sql
CREATE OR REPLACE FILE FORMAT csv_format
  TYPE = CSV
  PARSE_HEADER = TRUE
  FIELD_OPTIONALLY_ENCLOSED_BY = '"';

CREATE OR REPLACE TABLE COMPANIES
  USING TEMPLATE (
    SELECT ARRAY_AGG(OBJECT_CONSTRUCT(*))
    FROM TABLE(INFER_SCHEMA(
      LOCATION => '@HIIVE_AI.MARKETPLACE_OPS.DATA/companies.csv',
      FILE_FORMAT => 'csv_format'
    ))
  );

COPY INTO COMPANIES
  FROM @HIIVE_AI.MARKETPLACE_OPS.DATA/companies.csv
  FILE_FORMAT = csv_format;
```

**The 10 tables**:
| Table | Rows | Description |
|-------|------|-------------|
| COMPANIES | 25 | Pre-IPO companies on the platform (Stripe, SpaceX, etc.) |
| SHAREHOLDERS | 60 | Sellers with shares to trade |
| LISTINGS | 200 | Active and historical share listings |
| TRADE_EXECUTIONS | 350 | Completed secondary transactions |
| PRICING_SIGNALS | 150 | Valuation signals and 409A data |
| PLATFORM_ACTIVITY | 300 | Daily platform engagement metrics |
| USER_SESSIONS | 200 | User session and device data |
| COMPLIANCE_REVIEWS | 50 | KYC/AML and accreditation reviews |
| SUPPORT_TICKETS | 75 | Customer support interactions |
| REGULATORY_FILINGS | 50 | SEC Form D and other filings |
""")


PROMPT_1_3 = """Run a query in HIIVE_AI.MARKETPLACE_OPS that shows every table name and its row count, ordered by row count descending. Format it nicely."""

render_prompt("Prompt 1.3", "Verify All Data Tables", PROMPT_1_3)

render_explanation("What this prompt does", """
A quick verification query:

```sql
SELECT table_name, row_count
FROM HIIVE_AI.INFORMATION_SCHEMA.TABLES
WHERE table_schema = 'MARKETPLACE_OPS'
  AND table_type = 'BASE TABLE'
ORDER BY row_count DESC;
```

You should see approximately **1,460 total rows** across 10 tables.
""")


render_key_concepts([
    {"term": "Internal Stage", "definition": "A named Snowflake object that stores files within Snowflake's managed storage. Used to upload and reference files for loading via COPY INTO. Simpler than external stages when files are uploaded directly."},
    {"term": "INFER_SCHEMA", "definition": "A Snowflake table function that automatically detects column names and types from files in a stage. Eliminates manual CREATE TABLE DDL for well-structured CSV/Parquet files."},
    {"term": "File Format", "definition": "A named object specifying how to parse files (CSV delimiters, headers, quoting, compression). Created once and reused across multiple COPY INTO operations."},
])

render_what_you_built([
    "HIIVE_AI database and MARKETPLACE_OPS schema",
    "HIIVE_WH warehouse (Medium, auto-suspend 60s)",
    "10 marketplace data tables loaded from CSV (~1,460 total rows)",
])
