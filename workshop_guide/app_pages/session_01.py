import streamlit as st
from components import render_session_header, render_prompt, render_explanation, render_technologies_used, render_key_concepts, render_what_you_built, render_docs_links, render_execution_context

render_session_header(1, "Data Prep", "10:05 - 10:20 AM", "15 min", "Personal schema created and 10 marketplace tables loaded from shared stage")

render_technologies_used([
    {"name": "Schema & Stage", "description": "Each attendee creates their own schema (namespace) and personal stage inside the shared HIIVE_COCO_HOL database to avoid collisions with other participants.", "icon": "database"},
    {"name": "CSV File Format", "description": "Snowflake can infer schema and load data directly from CSV files using file formats and COPY INTO commands.", "icon": "table_chart"},
    {"name": "COPY FILES", "description": "Copies files between stages within Snowflake, allowing each attendee to get their own copy of the shared workshop data.", "icon": "file_copy"},
])


PROMPT_1_1 = """Set me up for the HIIVE CoCo HOL workshop.

I need you to:
1. Switch to the HIIVE_COCO_HOL_ROLE role and use the HIIVE_COCO_HOL_WH warehouse and HIIVE_COCO_HOL database
2. Create a personal schema for me using my Snowflake username (CURRENT_USER()) with an _OPS suffix — so if I'm logged in as OLEG, the schema should be OLEG_OPS
3. Inside that schema, create an internal stage called DATA with directory table enabled
4. Copy all the workshop CSV files from the shared stage at HIIVE_COCO_HOL.SHARED_DATA.WORKSHOP_FILES into my personal DATA stage

Execute everything and confirm what was created."""

render_prompt("Prompt 1.1", "Create Personal Schema & Stage", PROMPT_1_1)

st.markdown("""
> **Context check:** After running Prompt 1.1, verify your session is using `HIIVE_COCO_HOL_ROLE`, `HIIVE_COCO_HOL_WH`, and `HIIVE_COCO_HOL` database with your personal schema. In **Snowsight**, check the context selector in the top-left of the worksheet. In **Cortex Code (VS Code)**, the active connection is shown in the bottom status bar. If anything looks off, run:
> ```sql
> USE ROLE HIIVE_COCO_HOL_ROLE;
> USE WAREHOUSE HIIVE_COCO_HOL_WH;
> USE DATABASE HIIVE_COCO_HOL;
> USE SCHEMA <YOUR_USERNAME>_OPS;
> ```
""")

render_execution_context("cortex_code")

render_explanation("What this prompt does", """
Sets up your personal workspace within the shared `HIIVE_COCO_HOL` database:

```sql
USE ROLE HIIVE_COCO_HOL_ROLE;
USE WAREHOUSE HIIVE_COCO_HOL_WH;
USE DATABASE HIIVE_COCO_HOL;

-- Cortex Code resolves CURRENT_USER() and substitutes your username directly
-- e.g., CREATE SCHEMA IF NOT EXISTS OLEG_OPS;
SET MY_SCHEMA = CURRENT_USER() || '_OPS';
CREATE SCHEMA IF NOT EXISTS IDENTIFIER($MY_SCHEMA);
USE SCHEMA IDENTIFIER($MY_SCHEMA);

CREATE OR REPLACE STAGE DATA
  DIRECTORY = (ENABLE = TRUE)
  ENCRYPTION = (TYPE = 'SNOWFLAKE_SSE');

COPY FILES INTO @DATA
  FROM @HIIVE_COCO_HOL.SHARED_DATA.WORKSHOP_FILES;
```

**Why a personal schema?** Multiple attendees share the same `HIIVE_COCO_HOL` database. Using CURRENT_USER() to name the schema (e.g., `OLEG_OPS`, `SARAH_OPS`) means everyone works in their own namespace without object collisions — and no manual name substitution needed.

**COPY FILES** copies the 10 CSV files from the admin's shared stage into your personal `DATA` stage so you can load them into your own tables.

> **Note:** Cortex Code will typically resolve `CURRENT_USER()` and substitute your literal username (e.g., `CREATE SCHEMA IF NOT EXISTS OLEG_OPS`). The `IDENTIFIER()` function requires a session variable or literal string — it does not accept inline expressions like `CURRENT_USER() || '_OPS'` directly.
""")


PROMPT_1_2 = """Now load my workshop data. The 10 CSV files are in my personal DATA stage.

Create all 10 tables from these files: companies, shareholders, listings, trade_executions, pricing_signals, platform_activity, user_sessions, compliance_reviews, support_tickets, and regulatory_filings.

Use INFER_SCHEMA to automatically detect column types from the CSVs, create the tables, and load the data. Make sure the column names are uppercase. Use PARSE_HEADER=TRUE and FIELD_OPTIONALLY_ENCLOSED_BY='"' in the file format.

Execute everything and tell me how many rows loaded into each table."""

st.markdown("""
**Your personal stage already has the 10 CSV files** (copied in Prompt 1.1). Now we'll create tables and load the data.
""")

render_prompt("Prompt 1.2", "Load and Create Tables from CSV", PROMPT_1_2)

render_explanation("What this prompt does", """
Loads all 10 marketplace data tables from CSV files in your personal `DATA` stage. Cortex Code will use INFER_SCHEMA to detect column types automatically:

```sql
CREATE OR REPLACE FILE FORMAT csv_format
  TYPE = CSV
  PARSE_HEADER = TRUE
  FIELD_OPTIONALLY_ENCLOSED_BY = '"';

-- For each table, create with uppercase columns and load:
CREATE OR REPLACE TABLE COMPANIES
  USING TEMPLATE (
    SELECT ARRAY_AGG(OBJECT_CONSTRUCT(
      'COLUMN_NAME', UPPER("COLUMN_NAME"),
      'TYPE', "TYPE",
      'NULLABLE', "NULLABLE"
    ))
    FROM TABLE(INFER_SCHEMA(
      LOCATION => '@DATA/companies.csv',
      FILE_FORMAT => 'csv_format'
    ))
  );

COPY INTO COMPANIES
  FROM @DATA/companies.csv
  FILE_FORMAT = (FORMAT_NAME = 'csv_format')
  MATCH_BY_COLUMN_NAME = CASE_INSENSITIVE;
```

> **Why UPPER() in USING TEMPLATE?** INFER_SCHEMA preserves the CSV header casing (lowercase). Wrapping `COLUMN_NAME` in `UPPER()` ensures table columns are created as uppercase. `MATCH_BY_COLUMN_NAME = CASE_INSENSITIVE` then allows the COPY INTO to match lowercase CSV headers to uppercase table columns.

**The 10 tables**:
| Table | Rows | Description |
|-------|------|-------------|
| PLATFORM_ACTIVITY | 400 | Daily platform engagement metrics |
| TRADE_EXECUTIONS | 300 | Completed secondary transactions |
| USER_SESSIONS | 300 | User session and device data |
| LISTINGS | 200 | Active and historical share listings |
| PRICING_SIGNALS | 150 | Valuation signals and 409A data |
| COMPLIANCE_REVIEWS | 40 | KYC/AML and accreditation reviews |
| SHAREHOLDERS | 25 | Sellers with shares to trade |
| REGULATORY_FILINGS | 25 | SEC Form D and other filings |
| SUPPORT_TICKETS | 20 | Customer support interactions |
| COMPANIES | 15 | Pre-IPO companies on the platform (Stripe, SpaceX, etc.) |
""")


PROMPT_1_3 = """Show me all the tables in my schema with their row counts, ordered from largest to smallest. Format it as a clean table."""

render_prompt("Prompt 1.3", "Verify All Data Tables", PROMPT_1_3)

render_explanation("What this prompt does", """
A quick verification query:

```sql
SELECT table_name, row_count
FROM HIIVE_COCO_HOL.INFORMATION_SCHEMA.TABLES
WHERE table_schema = CURRENT_USER() || '_OPS'
  AND table_type = 'BASE TABLE'
ORDER BY row_count DESC;
```

You should see approximately **1,475 total rows** across 10 tables.
""")


render_key_concepts([
    {"term": "Personal Schema", "definition": "A namespace within a shared database where each attendee creates their own objects. Using CURRENT_USER() prevents naming collisions in multi-user workshops (e.g., OLEG_OPS, SARAH_OPS)."},
    {"term": "COPY FILES", "definition": "Copies files between Snowflake stages without downloading them. Used here to replicate shared workshop data into each attendee's personal stage."},
    {"term": "INFER_SCHEMA", "definition": "A Snowflake table function that automatically detects column names and types from files in a stage. Eliminates manual CREATE TABLE DDL for well-structured CSV/Parquet files."},
    {"term": "File Format", "definition": "A named object specifying how to parse files (CSV delimiters, headers, quoting, compression). Created once and reused across multiple COPY INTO operations."},
])

render_docs_links([
    {"title": "CREATE STAGE", "url": "https://docs.snowflake.com/en/sql-reference/sql/create-stage"},
    {"title": "COPY INTO <table>", "url": "https://docs.snowflake.com/en/sql-reference/sql/copy-into-table"},
    {"title": "File Formats", "url": "https://docs.snowflake.com/en/sql-reference/sql/create-file-format"},
    {"title": "COPY FILES", "url": "https://docs.snowflake.com/en/sql-reference/sql/copy-files"},
])

render_what_you_built([
    "Personal <YOUR_USERNAME>_OPS schema in HIIVE_COCO_HOL (created dynamically via CURRENT_USER())",
    "10 marketplace data tables loaded from shared stage (~1,475 total rows)",
])
