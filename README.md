# HIIVE CoCo Hands-On Lab — Preparation Guide

**Subject:** Action needed: Prep for Snowflake Cortex Code Workshop (July 16, 10:00 AM)

---

Hi team,

We have a hands-on lab with the Snowflake team on **July 16 at 10:00 AM** at the HIIVE office. The session covers Cortex Code (CoCo), Semantic Views, Cortex Search, Cortex Agents, Data Metric Functions for proactive monitoring, and **dbt Projects in Snowflake** (native alternative to GitHub Actions).

Below is what's needed from **Lauren (or whoever is running admin setup)** and what **each attendee** should have ready before we start.

---

## For the Champion / Admin (Lauren)

Run these **before July 16** so the environment is ready when attendees arrive.

### Snowflake Edition Recommendation

> DMFs (Data Metric Functions) — the proactive monitoring section — require **Enterprise Edition**. On our current Standard Edition, participants will not be able to do the DMF lab in Block 3 of the HOL. If we want full hands-on for Block 3, one recommendation is to temporarily create an enterprise account for this HOL.

### Setup Script (run as ACCOUNTADMIN)

**Step 0 — Download the workshop data files:**
> https://github.com/xavizone/coco-hol-hiive/tree/main/workshop_guide/data
>
> Download all 10 CSV files from the link above. You'll upload them to the shared stage in step 4.

**Step 0b — Download the dbt project files (for Session 8, Option A):**
> https://github.com/xavizone/coco-hol-hiive/tree/main/workshop_guide/dbt_project
>
> Download the entire `dbt_project/` folder. You'll upload it to the shared stage in step 5b. (Skip this if you plan to use Option B where Cortex Code generates the project live.)

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

-- 5a. Grant DMF privileges (Session 7: Data Metric Functions)
GRANT DATABASE ROLE SNOWFLAKE.DATA_METRIC_USER TO ROLE HIIVE_COCO_HOL_ROLE;
GRANT EXECUTE DATA METRIC FUNCTION ON ACCOUNT TO ROLE HIIVE_COCO_HOL_ROLE;

-- 5b. Session 8 (dbt Projects): Upload dbt project files to shared stage
-- Download from: https://github.com/xavizone/coco-hol-hiive/tree/main/workshop_guide/dbt_project
-- PUT file://./dbt_project/dbt_project.yml @HIIVE_COCO_HOL.SHARED_DATA.WORKSHOP_FILES/dbt_project/;
-- PUT file://./dbt_project/profiles.yml @HIIVE_COCO_HOL.SHARED_DATA.WORKSHOP_FILES/dbt_project/;
-- PUT file://./dbt_project/models/schema.yml @HIIVE_COCO_HOL.SHARED_DATA.WORKSHOP_FILES/dbt_project/models/;
-- PUT file://./dbt_project/models/staging/stg_trades.sql @HIIVE_COCO_HOL.SHARED_DATA.WORKSHOP_FILES/dbt_project/models/staging/;
-- PUT file://./dbt_project/models/staging/stg_listings.sql @HIIVE_COCO_HOL.SHARED_DATA.WORKSHOP_FILES/dbt_project/models/staging/;
-- PUT file://./dbt_project/models/marts/mart_company_performance.sql @HIIVE_COCO_HOL.SHARED_DATA.WORKSHOP_FILES/dbt_project/models/marts/;

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
- [ ] Upload the dbt_project/ folder to the shared stage (for Session 8, Option A)
- [ ] Verify `LIST @HIIVE_COCO_HOL.SHARED_DATA.WORKSHOP_FILES` shows 10 CSVs + 6 dbt project files
- [ ] Confirm each attendee can `USE ROLE HIIVE_COCO_HOL_ROLE` successfully
- [ ] (Recommended) Discuss Enterprise Edition upgrade with Snowflake team for full DMF hands-on
- [ ] Check Cortex Code works through Cloudflare VPN (if SSL cert errors occur, attendees add `insecure_mode = true` in `~/.snowflake/connections.toml`)

---

## For Attendees (Everyone)

### Install before the session

| What | How | Why |
|------|-----|-----|
| **Laptop with Chrome** | Bring it charged | We'll work in Snowsight (browser) for the full lab |
| **Snowflake CLI** | `brew install snowflake-cli` (Mac) | Required for Sessions 8-9 (dbt deploy/execute) and VS Code CoCo plugin |
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
- SSL/VPN issues with Cortex Code → If you're behind Cloudflare VPN and see SSL certificate errors, open `~/.snowflake/connections.toml` and add `insecure_mode = true` under your connection (e.g., `[default]`). This disables certificate verification for that connection. Example:
  ```toml
  [default]
  account = "your_account"
  user = "your_user"
  insecure_mode = true
  ```
- CLI install issues → the lab works entirely in-browser; CLI is only needed for VS Code plugin (optional)

---

## What we'll cover (~90 min)

| Block | Sessions | What you'll build |
|-------|----------|-------------------|
| **Block 1: Data & Intelligence** | Data Prep, Semantic Views, Cortex Search | 10 tables, a semantic view, a search service, and a RAG pipeline |
| **Block 2: Agents & Apps** | Cortex Agents, CoWork, Streamlit | An AI agent, collaborative analysis, and a live dashboard |
| **Block 3: Monitoring** | DMFs & Alerts | Anomaly detection DMFs and alerting (demo if Standard Edition) |
| **Block 4: Data Pipelines** | dbt Projects, dbt Hands-On | Native Snowflake dbt project — deploy, execute, version, rollback, and schedule with task chains (replaces GitHub Actions) |

### Edition note

| Edition | Block 3 experience |
|---------|-------------------|
| Standard (current) | Data Metric Functions (DMF) monitoring capability unavailable |
| Enterprise (recommended) | Full hands-on — create and schedule DMFs yourself |

---

Let me know if you have any questions. See you July 16!

— Xavier / Snowflake Team
