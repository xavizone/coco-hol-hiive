# HIIVE CoCo Hands-On Lab — Preparation Guide

**Subject:** Action needed: Prep for Snowflake Cortex Code Workshop (July 16, 10:00 AM)

---

Hi team,

We have a 90-minute hands-on lab with the Snowflake team on **July 16 at 10:00 AM** at the HIIVE office. The session covers Cortex Code (CoCo), Semantic Views, Cortex Search, Cortex Agents, and Data Metric Functions for proactive monitoring.

Below is what's needed from **Lauren (or whoever is running admin setup)** and what **each attendee** should have ready before we start.

---

## For the Champion / Admin (Lauren)

Run these **before July 16** so the environment is ready when attendees arrive.

### Snowflake Edition Recommendation

> DMFs (Data Metric Functions) — the proactive monitoring section — require **Enterprise Edition**. On our current Standard Edition, participants will not be able to do the DMF lab in Block 3 of the HOL. If we want full hands-on for Block 3, one recommendation is to temporarily create an enterprise account for this HOL.

### Setup Script (run as ACCOUNTADMIN)

```sql
-- 1. Create shared database
CREATE DATABASE IF NOT EXISTS HIIVE_COCO_HOL;
CREATE SCHEMA IF NOT EXISTS HIIVE_COCO_HOL.SHARED_DATA;

-- 2. Create shared warehouse
CREATE WAREHOUSE IF NOT EXISTS HIIVE_COCO_HOL_WH
  WAREHOUSE_SIZE = 'MEDIUM'
  AUTO_SUSPEND = 60
  AUTO_RESUME = TRUE;

-- 3. Create shared stage (upload CSVs here)
CREATE OR REPLACE STAGE HIIVE_COCO_HOL.SHARED_DATA.WORKSHOP_FILES
  DIRECTORY = (ENABLE = TRUE)
  ENCRYPTION = (TYPE = 'SNOWFLAKE_SSE');

-- 4. Upload the 10 CSV files to the stage
-- Download from: https://github.com/xavizone/coco-hol-hiive/tree/main/workshop_guide/data
-- Upload via Snowsight UI (Horizon Catalog → browse to stage) or SnowSQL:
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

-- 5. Create workshop role with necessary grants
CREATE ROLE IF NOT EXISTS HIIVE_COCO_HOL_ROLE;
GRANT USAGE ON DATABASE HIIVE_COCO_HOL TO ROLE HIIVE_COCO_HOL_ROLE;
GRANT USAGE ON SCHEMA HIIVE_COCO_HOL.SHARED_DATA TO ROLE HIIVE_COCO_HOL_ROLE;
GRANT READ ON STAGE HIIVE_COCO_HOL.SHARED_DATA.WORKSHOP_FILES TO ROLE HIIVE_COCO_HOL_ROLE;
GRANT CREATE SCHEMA ON DATABASE HIIVE_COCO_HOL TO ROLE HIIVE_COCO_HOL_ROLE;
GRANT USAGE ON WAREHOUSE HIIVE_COCO_HOL_WH TO ROLE HIIVE_COCO_HOL_ROLE;
GRANT DATABASE ROLE SNOWFLAKE.CORTEX_USER TO ROLE HIIVE_COCO_HOL_ROLE;

-- 6. Grant role to each attendee
GRANT ROLE HIIVE_COCO_HOL_ROLE TO USER OLEG;
GRANT ROLE HIIVE_COCO_HOL_ROLE TO USER LAUREN;
GRANT ROLE HIIVE_COCO_HOL_ROLE TO USER ABHI;
GRANT ROLE HIIVE_COCO_HOL_ROLE TO USER FERNANDO;
GRANT ROLE HIIVE_COCO_HOL_ROLE TO USER WENHAN;
-- Add any additional attendees here

-- 7. Create network rule + External Access Integration (for Streamlit pip packages)
CREATE OR REPLACE NETWORK RULE HIIVE_COCO_HOL.SHARED_DATA.PYPI_NETWORK_RULE
  MODE = EGRESS TYPE = HOST_PORT
  VALUE_LIST = ('pypi.org', 'files.pythonhosted.org');

CREATE OR REPLACE EXTERNAL ACCESS INTEGRATION HIIVE_COCO_HOL_PYPI_ACCESS
  ALLOWED_NETWORK_RULES = (HIIVE_COCO_HOL.SHARED_DATA.PYPI_NETWORK_RULE)
  ENABLED = TRUE;

GRANT USAGE ON INTEGRATION HIIVE_COCO_HOL_PYPI_ACCESS TO ROLE HIIVE_COCO_HOL_ROLE;

-- 8. Create compute pool for Streamlit apps
CREATE COMPUTE POOL IF NOT EXISTS HIIVE_COCO_HOL_COMPUTE_POOL
  MIN_NODES = 1
  MAX_NODES = 1
  INSTANCE_FAMILY = CPU_X64_S;

GRANT USAGE ON COMPUTE POOL HIIVE_COCO_HOL_COMPUTE_POOL TO ROLE HIIVE_COCO_HOL_ROLE;

-- 9. Enable cross-region inference
ALTER ACCOUNT SET CORTEX_ENABLED_CROSS_REGION = 'ANY_REGION';
```

### Admin Checklist

- [ ] Run the setup script above as ACCOUNTADMIN
- [ ] Upload all 10 CSV files to the shared stage
- [ ] Verify `LIST @HIIVE_COCO_HOL.SHARED_DATA.WORKSHOP_FILES` shows 10 files
- [ ] Confirm each attendee can `USE ROLE HIIVE_COCO_HOL_ROLE` successfully
- [ ] (Recommended) Discuss Enterprise Edition upgrade with Snowflake team for full DMF hands-on
- [ ] Check Cortex Code works through Cloudflare VPN (known SSL cert issue — may need trust store update)

---

## For Attendees (Everyone)

### Install before the session

| What | How | Why |
|------|-----|-----|
| **Laptop with Chrome** | Bring it charged | We'll work in Snowsight (browser) for the full lab |
| **Snowflake CLI** | `brew install snowflake-cli` (Mac) | Needed for VS Code CoCo plugin connectivity |
| **VS Code + Snowflake extension** | Extensions marketplace → search "Snowflake" → Install | Optional for the lab, but recommended for daily workflow after |
| **Claude Code CLI** | You already have this — run `claude update` to ensure latest | We'll reference CoCo as a complement to your existing Claude workflow |

### Verify day-of (before 10:00 AM)

1. **Log into Snowsight** with your HIIVE credentials
2. **Switch to the workshop role:**
   ```sql
   USE ROLE HIIVE_COCO_HOL_ROLE;
   USE WAREHOUSE HIIVE_COCO_HOL_WH;
   SELECT CURRENT_ROLE(), CURRENT_USER();
   ```
3. **Confirm you can see the shared data:**
   ```sql
   LIST @HIIVE_COCO_HOL.SHARED_DATA.WORKSHOP_FILES;
   ```
   You should see 10 CSV files.
4. **Open Cortex Code** from the left navigation panel in Snowsight
5. **That's it** — no manual naming needed. The lab uses `CURRENT_USER()` to create your personal schema automatically (e.g., `OLEG_OPS`)

### If something doesn't work

- Can't see the role → ask Lauren to run the GRANT for your username
- SSL/VPN issues with Cortex Code → set `insecure_mode = true` in your Snowflake connection config
- CLI install issues → the lab works entirely in-browser; CLI is only needed for VS Code plugin (optional)

---

## What we'll cover (90 min)

| Block | Sessions | What you'll build |
|-------|----------|-------------------|
| **Block 1: Data & Intelligence** | Data Prep, Semantic Views, Cortex Search | 10 tables, a semantic view, a search service, and a RAG pipeline |
| **Block 2: Agents & Apps** | Cortex Agents, CoWork, Streamlit | An AI agent, collaborative analysis, and a live dashboard |
| **Block 3: Monitoring** | DMFs & Alerts | Anomaly detection DMFs and alerting (demo if Standard Edition) |

### Edition note

| Edition | Block 3 experience |
|---------|-------------------|
| Standard (current) | Data Metric Functions (DMF) monitoring capability unavailable |
| Enterprise (recommended) | Full hands-on — create and schedule DMFs yourself |

---

Let me know if you have any questions. See you July 16!

— Xavier / Snowflake Team
