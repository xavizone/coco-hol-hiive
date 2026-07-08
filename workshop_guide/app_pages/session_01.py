import streamlit as st
from components import render_session_header, render_prompt, render_explanation, render_technologies_used, render_key_concepts, render_what_you_built

render_session_header(1, "Data Prep", "10:00 - 10:25 AM", "25 min", "Personal schema created and 10 marketplace tables loaded from shared stage")

render_technologies_used([
    {"name": "Schema & Stage", "description": "Each attendee creates their own schema (namespace) and personal stage inside the shared HIIVE_COCO_HOL database to avoid collisions with other participants.", "icon": "database"},
    {"name": "CSV File Format", "description": "Snowflake can infer schema and load data directly from CSV files using file formats and COPY INTO commands.", "icon": "table_chart"},
    {"name": "COPY FILES", "description": "Copies files between stages within Snowflake, allowing each attendee to get their own copy of the shared workshop data.", "icon": "file_copy"},
])


PROMPT_1_1 = """Create your personal schema for the workshop. Use CURRENT_USER() to name it automatically:

1. Set session context:
   USE ROLE HIIVE_COCO_HOL_ROLE;
   USE WAREHOUSE HIIVE_COCO_HOL_WH;
   USE DATABASE HIIVE_COCO_HOL;

2. Create your personal schema named after your Snowflake username:
   CREATE SCHEMA IF NOT EXISTS IDENTIFIER(CURRENT_USER() || '_OPS');
   USE SCHEMA IDENTIFIER(CURRENT_USER() || '_OPS');

3. Create a personal stage and copy workshop data:
   CREATE OR REPLACE STAGE DATA DIRECTORY = (ENABLE = TRUE) ENCRYPTION = (TYPE = 'SNOWFLAKE_SSE');
   COPY FILES INTO @DATA FROM @HIIVE_COCO_HOL.SHARED_DATA.WORKSHOP_FILES;

Execute all SQL and confirm."""

render_prompt("Prompt 1.1", "Create Personal Schema & Stage", PROMPT_1_1)

render_explanation("What this prompt does", """
Sets up your personal workspace within the shared `HIIVE_COCO_HOL` database:

```sql
USE ROLE HIIVE_COCO_HOL_ROLE;
USE WAREHOUSE HIIVE_COCO_HOL_WH;
USE DATABASE HIIVE_COCO_HOL;

CREATE SCHEMA IF NOT EXISTS IDENTIFIER(CURRENT_USER() || '_OPS');
USE SCHEMA IDENTIFIER(CURRENT_USER() || '_OPS');

CREATE OR REPLACE STAGE DATA
  DIRECTORY = (ENABLE = TRUE)
  ENCRYPTION = (TYPE = 'SNOWFLAKE_SSE');

COPY FILES INTO @DATA
  FROM @HIIVE_COCO_HOL.SHARED_DATA.WORKSHOP_FILES;
```

**Why a personal schema?** Multiple attendees share the same `HIIVE_COCO_HOL` database. Using CURRENT_USER() to name the schema (e.g., `OLEG_OPS`, `SARAH_OPS`) means everyone works in their own namespace without object collisions — and no manual name substitution needed.

**COPY FILES** copies the 10 CSV files from the admin's shared stage into your personal `DATA` stage so you can load them into your own tables.
""")


PROMPT_1_2 = """In your workshop schema in HIIVE_COCO_HOL, the 10 CSV files are now in your personal DATA stage.

For all 10 tables (COMPANIES, SHAREHOLDERS, LISTINGS, TRADE_EXECUTIONS, PRICING_SIGNALS, PLATFORM_ACTIVITY, USER_SESSIONS, COMPLIANCE_REVIEWS, SUPPORT_TICKETS, REGULATORY_FILINGS):

1. Create a file format (CSV with PARSE_HEADER=TRUE, FIELD_OPTIONALLY_ENCLOSED_BY='"')
2. Create the tables with appropriate column types inferred from the data. Ensure to convert the column names to uppercase.
3. Load the data

Use CREATE TABLE with INFER_SCHEMA from a stage and then COPY INTO them. The key requirement is that all 10 tables are created and populated.

Execute all SQL."""

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

CREATE OR REPLACE TABLE COMPANIES
  USING TEMPLATE (
    SELECT ARRAY_AGG(OBJECT_CONSTRUCT(*))
    FROM TABLE(INFER_SCHEMA(
      LOCATION => '@DATA/companies.csv',
      FILE_FORMAT => 'csv_format'
    ))
  );

COPY INTO COMPANIES
  FROM @DATA/companies.csv
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


PROMPT_1_3 = """Run a query in HIIVE_COCO_HOL that shows every table name and its row count in your schema, ordered by row count descending. Format it nicely."""

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

You should see approximately **1,460 total rows** across 10 tables.
""")


render_key_concepts([
    {"term": "Personal Schema", "definition": "A namespace within a shared database where each attendee creates their own objects. Using CURRENT_USER() prevents naming collisions in multi-user workshops (e.g., OLEG_OPS, SARAH_OPS)."},
    {"term": "COPY FILES", "definition": "Copies files between Snowflake stages without downloading them. Used here to replicate shared workshop data into each attendee's personal stage."},
    {"term": "INFER_SCHEMA", "definition": "A Snowflake table function that automatically detects column names and types from files in a stage. Eliminates manual CREATE TABLE DDL for well-structured CSV/Parquet files."},
    {"term": "File Format", "definition": "A named object specifying how to parse files (CSV delimiters, headers, quoting, compression). Created once and reused across multiple COPY INTO operations."},
])

render_what_you_built([
    "Personal <username>_OPS schema in HIIVE_COCO_HOL (created dynamically via CURRENT_USER())",
    "10 marketplace data tables loaded from shared stage (~1,460 total rows)",
])
