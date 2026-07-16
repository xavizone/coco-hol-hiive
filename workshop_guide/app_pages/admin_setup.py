import streamlit as st

st.title("Lab Setup — Admin Only")
st.markdown("Environment setup to run **once before the workshop**")

st.warning("This page is for the **workshop admin** only. Attendees should go to **Getting Started** instead.", icon=":material/admin_panel_settings:")

# ─────────────────────────────────────────────────────────────────────────────
# Section A: Admin Pre-Setup
# ─────────────────────────────────────────────────────────────────────────────

st.space("small")
st.markdown("## :material/admin_panel_settings: Admin Pre-Setup (Run Once Before Workshop)")

with st.container(border=True):
    st.markdown("""
The admin creates the shared database, warehouse, stage, and role that all attendees will use.
Run the following SQL as **ACCOUNTADMIN** (or a role with sufficient privileges):
""")

    st.code("""-- 0. Set ACCOUNTADMIN role to run the setup
USE ROLE ACCOUNTADMIN;

-- 1. Create the workshop warehouse
CREATE WAREHOUSE IF NOT EXISTS HIIVE_COCO_HOL_WH
  WAREHOUSE_SIZE = 'MEDIUM'
  AUTO_SUSPEND = 60
  AUTO_RESUME = TRUE;

-- 2. Create the shared database
CREATE DATABASE IF NOT EXISTS HIIVE_COCO_HOL;

-- 3. Create a shared schema for common resources
CREATE SCHEMA IF NOT EXISTS HIIVE_COCO_HOL.SHARED_DATA;

-- 4. Create a shared stage and upload the 10 CSV files
-- Download CSVs to a local folder from: https://github.com/xavizone/coco-hol-hiive/tree/main/workshop_guide/Workshop_Data_Assets/csv_data
CREATE OR REPLACE STAGE HIIVE_COCO_HOL.SHARED_DATA.WORKSHOP_FILES
  DIRECTORY = (ENABLE = TRUE)
  ENCRYPTION = (TYPE = 'SNOWFLAKE_SSE');

-- **Loading the CSV files can be done in two ways:**

-- Option 1: Snowsight UI — drag and drop the 10 CSV files into the stage (use database explorer to navigate to the stage)

-- Option 2: SnowSQL — Run the below commands to upload the files (replace `<path_to_csvs>` with your local path)           
  -- Tip: You can also use a wildcard (e.g., `file://<path_to_csvs>/*.csv`) to upload all CSVs at once.
    -- PUT 'file://<folder_path_to_csvs>/companies.csv' @HIIVE_COCO_HOL.SHARED_DATA.WORKSHOP_FILES;
    -- PUT 'file://<folder_path_to_csvs>/shareholders.csv' @HIIVE_COCO_HOL.SHARED_DATA.WORKSHOP_FILES;
    -- PUT 'file://<folder_path_to_csvs>/listings.csv' @HIIVE_COCO_HOL.SHARED_DATA.WORKSHOP_FILES;
    -- PUT 'file://<folder_path_to_csvs>/trade_executions.csv' @HIIVE_COCO_HOL.SHARED_DATA.WORKSHOP_FILES;
    -- PUT 'file://<folder_path_to_csvs>/pricing_signals.csv' @HIIVE_COCO_HOL.SHARED_DATA.WORKSHOP_FILES;
    -- PUT 'file://<folder_path_to_csvs>/platform_activity.csv' @HIIVE_COCO_HOL.SHARED_DATA.WORKSHOP_FILES;
    -- PUT 'file://<folder_path_to_csvs>/user_sessions.csv' @HIIVE_COCO_HOL.SHARED_DATA.WORKSHOP_FILES;
    -- PUT 'file://<folder_path_to_csvs>/compliance_reviews.csv' @HIIVE_COCO_HOL.SHARED_DATA.WORKSHOP_FILES;
    -- PUT 'file://<folder_path_to_csvs>/support_tickets.csv' @HIIVE_COCO_HOL.SHARED_DATA.WORKSHOP_FILES;
    -- PUT 'file://<folder_path_to_csvs>/regulatory_filings.csv' @HIIVE_COCO_HOL.SHARED_DATA.WORKSHOP_FILES;


-- 5. Create network rule and EAI for Streamlit apps (requires ACCOUNTADMIN)
CREATE OR REPLACE NETWORK RULE HIIVE_COCO_HOL.SHARED_DATA.PYPI_NETWORK_RULE
  MODE = EGRESS TYPE = HOST_PORT
  VALUE_LIST = ('pypi.org', 'files.pythonhosted.org');

CREATE OR REPLACE EXTERNAL ACCESS INTEGRATION HIIVE_COCO_HOL_PYPI_ACCESS
  ALLOWED_NETWORK_RULES = (HIIVE_COCO_HOL.SHARED_DATA.PYPI_NETWORK_RULE)
  ENABLED = TRUE;
            

-- 6. Create a compute pool for Session 6 (Streamlit app)
CREATE COMPUTE POOL IF NOT EXISTS HIIVE_COCO_HOL_COMPUTE_POOL
  MIN_NODES = 1
  MAX_NODES = 1
  INSTANCE_FAMILY = CPU_X64_S;

            
-- 7. Create a workshop role and grant privileges
CREATE ROLE IF NOT EXISTS HIIVE_COCO_HOL_ROLE;
GRANT USAGE ON DATABASE HIIVE_COCO_HOL TO ROLE HIIVE_COCO_HOL_ROLE;
GRANT USAGE ON SCHEMA HIIVE_COCO_HOL.SHARED_DATA TO ROLE HIIVE_COCO_HOL_ROLE;
GRANT READ ON STAGE HIIVE_COCO_HOL.SHARED_DATA.WORKSHOP_FILES TO ROLE HIIVE_COCO_HOL_ROLE;
GRANT CREATE SCHEMA ON DATABASE HIIVE_COCO_HOL TO ROLE HIIVE_COCO_HOL_ROLE;
GRANT USAGE ON WAREHOUSE HIIVE_COCO_HOL_WH TO ROLE HIIVE_COCO_HOL_ROLE;
GRANT USAGE ON COMPUTE POOL HIIVE_COCO_HOL_COMPUTE_POOL TO ROLE HIIVE_COCO_HOL_ROLE;
GRANT USAGE ON INTEGRATION HIIVE_COCO_HOL_PYPI_ACCESS TO ROLE HIIVE_COCO_HOL_ROLE;

-- Grant Cortex and AI object creation privileges
GRANT DATABASE ROLE SNOWFLAKE.CORTEX_USER TO ROLE HIIVE_COCO_HOL_ROLE;
GRANT CREATE SNOWFLAKE.ML.ANOMALY_DETECTION ON SCHEMA HIIVE_COCO_HOL.SHARED_DATA TO ROLE HIIVE_COCO_HOL_ROLE;

-- Grant DMF privileges (Session 7: Data Metric Functions & Monitoring)
GRANT DATABASE ROLE SNOWFLAKE.DATA_METRIC_USER TO ROLE HIIVE_COCO_HOL_ROLE;
GRANT EXECUTE DATA METRIC FUNCTION ON ACCOUNT TO ROLE HIIVE_COCO_HOL_ROLE;

-- Grant per-user schema privileges (these apply once users create their schemas)
-- Users need: CREATE TABLE, CREATE VIEW, CREATE STAGE, CREATE FUNCTION,
-- CREATE CORTEX SEARCH SERVICE, CREATE STREAMLIT, CREATE DBT PROJECT, CREATE TASK in their own schemas
-- CREATE SCHEMA already grants these implicitly on schemas the role creates

-- 8. Grant the workshop role to each attendee (run once per user)
GRANT ROLE HIIVE_COCO_HOL_ROLE TO USER <each_attendee>;


-- 9. Enable cross-region inference (requires ACCOUNTADMIN)
ALTER ACCOUNT SET CORTEX_ENABLED_CROSS_REGION = 'ANY_REGION';""", language="sql")

    st.markdown("""
**Notes:**
- Replace `<each_attendee>` with each workshop participant's username (one GRANT per user)
- Download the 10 CSV files from: [github.com/xavizone/coco-hol-hiive/tree/main/workshop_guide/Workshop_Data_Assets/csv_data](https://github.com/xavizone/coco-hol-hiive/tree/main/workshop_guide/Workshop_Data_Assets/csv_data)
- Cross-region inference allows Cortex LLM requests to route to the nearest available region
""")

# ─────────────────────────────────────────────────────────────────────────────
# Section A.1: Session 8 (dbt Projects) Setup
# ─────────────────────────────────────────────────────────────────────────────

st.space("small")

st.markdown("#### :material/transform: Session 8 Setup: dbt Project Files")

with st.container(border=True):
    st.markdown("""
**For Option A (Pre-built from Stage):** Upload the workshop dbt project files to the shared stage so attendees can copy and deploy them. This step is **not required** if you plan to use Option B (where Cortex Code generates the dbt project live).

Download the `dbt_project/` folder from:
[github.com/xavizone/coco-hol-hiive/tree/main/workshop_guide/Workshop_Data_Assets/dbt_project](https://github.com/xavizone/coco-hol-hiive/tree/main/workshop_guide/Workshop_Data_Assets/dbt_project)
""")

    st.code("""-- Upload dbt project files to shared stage (preserving folder structure)
-- Run as ACCOUNTADMIN or a role with WRITE access to the stage
-- Replace `<local_path>/local_folder_path` with the local path to the downloaded `dbt_project/` folder
-- **Loading the dbt project files can be done in two ways:**

-- Option 1: Snowsight UI — drag and drop (use database explorer to navigate to the stage)

-- Option 2: Use SnowSQL — Run the below commands to upload the files
    -- These commands preserve the folder structure in the stage so that dbt can find the files correctly.
    -- Commands work only if the local folder structure matches the dbt project structure (e.g., `dbt_project.yml` at root, `models/` subfolder, etc.)
    -- Tip: You can also use a wildcard (e.g., `file://<local_folder_path>/models/**/*.sql`) to upload all SQL files at once.
    -- These commands work only in SnowSQL or Snowsight SQL editor, not in the CoCo plugin.
        PUT 'file://<local_folder_path>/dbt_project.yml' @HIIVE_COCO_HOL.SHARED_DATA.WORKSHOP_FILES/dbt_project/;
        PUT 'file://<local_folder_path>/profiles.yml' @HIIVE_COCO_HOL.SHARED_DATA.WORKSHOP_FILES/dbt_project/;
        PUT 'file://<local_folder_path>/models/schema.yml' @HIIVE_COCO_HOL.SHARED_DATA.WORKSHOP_FILES/dbt_project/models/;
        PUT 'file://<local_folder_path>/models/staging/stg_trades.sql' @HIIVE_COCO_HOL.SHARED_DATA.WORKSHOP_FILES/dbt_project/models/staging/;
        PUT 'file://<local_folder_path>/models/staging/stg_listings.sql' @HIIVE_COCO_HOL.SHARED_DATA.WORKSHOP_FILES/dbt_project/models/staging/;
        PUT 'file://<local_folder_path>/models/marts/mart_company_performance.sql' @HIIVE_COCO_HOL.SHARED_DATA.WORKSHOP_FILES/dbt_project/models/marts/;

-- Verify upload
LIST @HIIVE_COCO_HOL.SHARED_DATA.WORKSHOP_FILES/dbt_project/;
-- Should show 6 files across the folder structure""", language="sql")

    st.markdown("""
**Verify:** `LIST @HIIVE_COCO_HOL.SHARED_DATA.WORKSHOP_FILES/dbt_project/` should return 6 files.

**Note:** The `HIIVE_COCO_HOL_ROLE` already has READ access to the shared stage (granted in the main setup above). No additional grants are needed — attendees can copy files from this stage to their personal stage and deploy using `snow dbt deploy`.
""")

# ─────────────────────────────────────────────────────────────────────────────
# Section A.2: Cleanup Script
# ─────────────────────────────────────────────────────────────────────────────

st.space("small")

st.markdown("#### :material/delete: Cleanup Script (Reset for Repeat Labs)")

with st.container(border=True):
    st.markdown("""
Run this script to clean up all workshop objects and reset the environment for another run. This drops all user schemas created during the lab while preserving the shared infrastructure.

:material/warning: **This will permanently delete all attendee work.** Only run between lab sessions.
""")
    st.code("""-- ============================================
-- HIIVE CoCo HOL Cleanup Script
-- Run this between lab sessions to reset
-- ============================================

USE ROLE ACCOUNTADMIN;
USE DATABASE HIIVE_COCO_HOL;

-- Drop all user schemas (attendee work)
-- Each attendee created <USERNAME>_OPS
SHOW SCHEMAS IN DATABASE HIIVE_COCO_HOL;

-- Programmatic cleanup: drop all schemas ending in _OPS except SHARED_DATA and INFORMATION_SCHEMA
DECLARE
  c1 CURSOR FOR
    SELECT schema_name FROM HIIVE_COCO_HOL.INFORMATION_SCHEMA.SCHEMATA
    WHERE schema_name LIKE '%_OPS'
      AND schema_name != 'SHARED_DATA';
  schema_name VARCHAR;
BEGIN
  OPEN c1;
  LOOP
    FETCH c1 INTO schema_name;
    IF (c1%NOTFOUND) THEN LEAVE; END IF;
    EXECUTE IMMEDIATE 'DROP SCHEMA IF EXISTS HIIVE_COCO_HOL.' || :schema_name || ' CASCADE';
  END LOOP;
  CLOSE c1;
END;

-- Suspend the warehouse (save credits)
ALTER WAREHOUSE HIIVE_COCO_HOL_WH SUSPEND;

-- Suspend the compute pool
ALTER COMPUTE POOL HIIVE_COCO_HOL_COMPUTE_POOL SUSPEND;

-- (Optional) Full teardown — removes EVERYTHING including shared data
-- Only use if the lab will never be repeated on this account:
-- DROP DATABASE IF EXISTS HIIVE_COCO_HOL CASCADE;
-- DROP WAREHOUSE IF EXISTS HIIVE_COCO_HOL_WH;
-- DROP COMPUTE POOL IF NOT EXISTS HIIVE_COCO_HOL_COMPUTE_POOL;
-- DROP ROLE IF EXISTS HIIVE_COCO_HOL_ROLE;
""", language="sql")
