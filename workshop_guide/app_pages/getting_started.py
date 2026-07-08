import streamlit as st

st.title("Getting Started")
st.markdown("Workshop environment setup and attendee prerequisites")

# ─────────────────────────────────────────────────────────────────────────────
# Section A: Admin Pre-Setup
# ─────────────────────────────────────────────────────────────────────────────

st.space("small")
st.markdown("## :material/admin_panel_settings: Admin Pre-Setup (Run Once Before Workshop)")

st.info("This section is for the **HIIVE admin** (or Snowflake team) to run **before** the workshop begins. Attendees can skip to Section B below.", icon=":material/info:")

with st.container(border=True):
    st.markdown("""
The admin creates the shared database, warehouse, stage, and role that all attendees will use.
Run the following SQL as **ACCOUNTADMIN** (or a role with sufficient privileges):
""")

    st.code("""-- 1. Create the shared database
CREATE DATABASE IF NOT EXISTS HIIVE_COCO_HOL;

-- 2. Create a shared schema for common resources
CREATE SCHEMA IF NOT EXISTS HIIVE_COCO_HOL.SHARED_DATA;

-- 3. Create the workshop warehouse
CREATE WAREHOUSE IF NOT EXISTS HIIVE_COCO_HOL_WH
  WAREHOUSE_SIZE = 'MEDIUM'
  AUTO_SUSPEND = 60
  AUTO_RESUME = TRUE;

-- 4. Create a shared stage and upload the 10 CSV files
-- Download CSVs from: https://github.com/xavizone/coco-hol-hiive/tree/main/workshop_guide/data
CREATE OR REPLACE STAGE HIIVE_COCO_HOL.SHARED_DATA.WORKSHOP_FILES
  DIRECTORY = (ENABLE = TRUE)
  ENCRYPTION = (TYPE = 'SNOWFLAKE_SSE');

-- Upload all 10 CSV files to this stage via Snowsight UI or SnowSQL:
-- PUT file://./companies.csv @HIIVE_COCO_HOL.SHARED_DATA.WORKSHOP_FILES;
-- PUT file://./shareholders.csv @HIIVE_COCO_HOL.SHARED_DATA.WORKSHOP_FILES;
-- PUT file://./listings.csv @HIIVE_COCO_HOL.SHARED_DATA.WORKSHOP_FILES;
-- PUT file://./trade_executions.csv @HIIVE_COCO_HOL.SHARED_DATA.WORKSHOP_FILES;
-- PUT file://./pricing_signals.csv @HIIVE_COCO_HOL.SHARED_DATA.WORKSHOP_FILES;
-- PUT file://./platform_activity.csv @HIIVE_COCO_HOL.SHARED_DATA.WORKSHOP_FILES;
-- PUT file://./user_sessions.csv @HIIVE_COCO_HOL.SHARED_DATA.WORKSHOP_FILES;
-- PUT file://./compliance_reviews.csv @HIIVE_COCO_HOL.SHARED_DATA.WORKSHOP_FILES;
-- PUT file://./support_tickets.csv @HIIVE_COCO_HOL.SHARED_DATA.WORKSHOP_FILES;
-- PUT file://./regulatory_filings.csv @HIIVE_COCO_HOL.SHARED_DATA.WORKSHOP_FILES;

-- 5. Create a workshop role and grant privileges
CREATE ROLE IF NOT EXISTS HIIVE_COCO_HOL_ROLE;
GRANT USAGE ON DATABASE HIIVE_COCO_HOL TO ROLE HIIVE_COCO_HOL_ROLE;
GRANT USAGE ON SCHEMA HIIVE_COCO_HOL.SHARED_DATA TO ROLE HIIVE_COCO_HOL_ROLE;
GRANT READ ON STAGE HIIVE_COCO_HOL.SHARED_DATA.WORKSHOP_FILES TO ROLE HIIVE_COCO_HOL_ROLE;
GRANT CREATE SCHEMA ON DATABASE HIIVE_COCO_HOL TO ROLE HIIVE_COCO_HOL_ROLE;
GRANT USAGE ON WAREHOUSE HIIVE_COCO_HOL_WH TO ROLE HIIVE_COCO_HOL_ROLE;
GRANT ROLE HIIVE_COCO_HOL_ROLE TO USER <each_attendee>;

-- 6. Create a compute pool for Session 6 (Streamlit app)
CREATE COMPUTE POOL IF NOT EXISTS HIIVE_COCO_HOL_COMPUTE_POOL
  MIN_NODES = 1
  MAX_NODES = 1
  INSTANCE_FAMILY = CPU_X64_S;

-- 7. Enable cross-region inference (requires ACCOUNTADMIN)
USE ROLE ACCOUNTADMIN;
ALTER ACCOUNT SET CORTEX_ENABLED_CROSS_REGION = 'ANY_REGION';""", language="sql")

    st.markdown("""
**Notes:**
- Replace `<each_attendee>` with each workshop participant's username (one GRANT per user)
- Download the 10 CSV files from: [github.com/xavizone/coco-hol-hiive/tree/main/workshop_guide/data](https://github.com/xavizone/coco-hol-hiive/tree/main/workshop_guide/data)
- Cross-region inference allows Cortex LLM requests to route to the nearest available region
""")

# ─────────────────────────────────────────────────────────────────────────────
# Section A.1: Cleanup Script
# ─────────────────────────────────────────────────────────────────────────────

st.space("small")

st.markdown("#### Cleanup Script (Reset for Repeat Labs)")

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

-- Drop each user schema (run for each attendee or use a script)
-- Example: DROP SCHEMA IF EXISTS OLEG_OPS;
-- Example: DROP SCHEMA IF EXISTS LAUREN_OPS;
-- Example: DROP SCHEMA IF EXISTS ABHI_OPS;
-- Example: DROP SCHEMA IF EXISTS FERNANDO_OPS;

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

# ─────────────────────────────────────────────────────────────────────────────
# Section B: Attendee Prerequisites
# ─────────────────────────────────────────────────────────────────────────────

st.space("small")
st.markdown("## :material/person: Attendee Prerequisites (Before You Start)")

st.markdown("Confirm the following before the lab begins:")

st.markdown("#### 1. Verify login")
with st.container(border=True):
    st.markdown("Log into **Snowsight** with your HIIVE credentials and confirm you have access.")

st.markdown("#### 2. Check role")
with st.container(border=True):
    st.markdown("Confirm you have `HIIVE_COCO_HOL_ROLE` assigned:")
    st.code("""USE ROLE HIIVE_COCO_HOL_ROLE;
USE WAREHOUSE HIIVE_COCO_HOL_WH;
SELECT CURRENT_ROLE(), CURRENT_USER();""", language="sql")

st.markdown("#### 3. Verify shared resources are visible")
with st.container(border=True):
    st.markdown("Run the following to confirm the shared stage is accessible:")
    st.code("LIST @HIIVE_COCO_HOL.SHARED_DATA.WORKSHOP_FILES;", language="sql")
    st.markdown("You should see **10 CSV files** listed.")

st.markdown("#### 4. Understand the naming convention")
with st.container(border=True):
    st.markdown("""
Your personal schema will be created automatically using your Snowflake username (e.g., if you're logged in as OLEG, your schema will be `HIIVE_COCO_HOL.OLEG_OPS`).

This prevents object collisions between attendees — everyone works in their own namespace.
""")

st.markdown("#### 5. Open Cortex Code")
with st.container(border=True):
    st.markdown("""
In Snowsight, open **Cortex Code** from the left navigation panel. This is where you'll paste all prompts from this workshop.

You can check and switch roles in the bottom-left of the Snowsight UI.
""")

st.markdown("#### 6. (Optional) VS Code Plugin")
with st.container(border=True):
    st.markdown("""
If you'd like to use Cortex Code from VS Code:

1. Open VS Code → Extensions → search **"Snowflake"** → Install
2. Command Palette (`Cmd+Shift+P`) → **"Snowflake: Sign In"**
3. Configure your connection in `~/.snowflake/connections.toml`

See the **Reference** page in the sidebar for full setup details.

:material/warning: **Cloudflare VPN note**: If you encounter SSL certificate issues, you may need to set `insecure_mode = true` in your connection config or add Cloudflare's root cert to the trust store.
""")

# ─────────────────────────────────────────────────────────────────────────────
# Summary
# ─────────────────────────────────────────────────────────────────────────────

st.space("small")
st.divider()

st.markdown("#### Quick reference")

col1, col2, col3 = st.columns(3)
col1.metric("Role", "HIIVE_COCO_HOL_ROLE", help="Pre-assigned by admin")
col2.metric("Warehouse", "HIIVE_COCO_HOL_WH", help="Shared Medium warehouse")
col3.metric("Duration", "90 min", help="Starting at 10:00 AM")

st.caption("All prompts build sequentially — run them in order. Once you've confirmed access, you're ready to start Session 1.")
