import streamlit as st
from components import render_session_header, render_prompt, render_explanation, render_technologies_used, render_key_concepts, render_what_you_built, render_docs_links, render_execution_context

render_session_header(8, "dbt Projects", "11:25 - 11:45 AM", "20 min", "Migrate, deploy, execute, and schedule a dbt project natively in Snowflake")

render_technologies_used([
    {"name": "Snowflake-native dbt", "description": "Deploy dbt projects as first-class Snowflake objects. SQL models stay identical — only the orchestration layer moves into Snowflake. No external runner or CI system required.", "icon": "integration_instructions"},
    {"name": "EXECUTE DBT PROJECT", "description": "Native SQL command that runs dbt builds on Snowflake warehouse compute. Supports build, run, test, and seed commands with full dbt semantics.", "icon": "play_circle"},
    {"name": "Snowflake Tasks", "description": "CRON-based scheduling that replaces GitHub Actions triggers entirely. One SQL statement replaces an entire .github/workflows/dbt.yml file.", "icon": "schedule"},
])

st.info("""
:material/swap_horiz: **Migration Context: What Changes vs What Stays**

Your SQL models stay exactly the same — zero changes. Only the orchestration layer moves into Snowflake.

| What | Before (GitHub Actions) | After (Snowflake Native) |
|------|------------------------|--------------------------|
| **profiles.yml** | Has password, env_var() | Remove auth fields (session handles it) |
| **SQL models** | models/*.sql | Exactly the same — zero changes |
| **dbt_project.yml** | May have env_var() | Replace with literal values |
| **Orchestration** | .github/workflows/dbt.yml | Snowflake Task (1 SQL statement) |
| **Execution** | GitHub runner → dbt run | EXECUTE DBT PROJECT on Snowflake compute |

**The pipeline shift:**
- **Current**: GitHub repo → GH Actions trigger → external runner → `dbt run` → Snowflake
- **Native**: `snow dbt deploy` → project lives IN Snowflake → `EXECUTE DBT PROJECT` on Snowflake compute → Snowflake Task for scheduling
""")

st.markdown("---")

st.caption(":material/terminal: Commands prefixed with `snow` require the **Snowflake CLI**. SQL commands (CREATE TASK, EXECUTE DBT PROJECT) can run in **Snowsight** or **Cortex Code**.")

# Define shared prompts (identical across both options)
PROMPT_8_2 = """Run our deployed HIIVE_MARKETPLACE dbt project. I need you to:

1. Execute a full build (models + tests): snow dbt execute -c default --database HIIVE_COCO_HOL --schema <YOUR_USERNAME>_OPS HIIVE_MARKETPLACE build
2. Show me the results — how many models passed, how many tests passed
3. Query the newly created mart table (MART_COMPANY_PERFORMANCE) to show company metrics
4. Verify all expected objects exist: STG_TRADES (view), STG_LISTINGS (view), MART_COMPANY_PERFORMANCE (table)

Execute and show the results."""

PROMPT_8_3 = """Now replace our GitHub Actions workflow with a native Snowflake Task. I need you to:

1. Create a Snowflake Task called DBT_HOURLY_BUILD in my schema that:
   - Uses the HIIVE_COCO_HOL_WH warehouse
   - Runs on a CRON schedule every hour (USING CRON 0 * * * * America/Vancouver)
   - Executes: EXECUTE DBT PROJECT HIIVE_COCO_HOL.<YOUR_USERNAME>_OPS.HIIVE_MARKETPLACE ARGS = 'build'
2. Resume the task so it starts running
3. Show me the task details to confirm it's active

Execute everything. This single Task replaces our entire .github/workflows/dbt.yml file."""

PROMPT_8_4 = """Show me how to monitor our dbt project execution without leaving Snowflake. I need you to:

1. Show all versions of the deployed project: SHOW VERSIONS IN DBT PROJECT HIIVE_COCO_HOL.<YOUR_USERNAME>_OPS.HIIVE_MARKETPLACE
2. Query the task execution history for our DBT_HOURLY_BUILD task (last 10 runs)
3. Show me how to check if any dbt tests failed in the most recent run
4. Describe the dbt project to see its metadata

Execute all queries and explain how this replaces checking GitHub Actions logs."""

# Two options via tabs
tab_a, tab_b = st.tabs(["Option A: Pre-built from Stage", "Option B: CoCo Generates Live"])

with tab_a:
    st.caption("Use the pre-staged dbt project files prepared by the workshop admin.")

    PROMPT_8A_1 = """The workshop admin has pre-staged a dbt project in our shared stage. I need you to:

1. Copy the dbt project files from @HIIVE_COCO_HOL.SHARED_DATA.WORKSHOP_FILES/dbt_project/ into my personal DATA stage
2. Show me the profiles.yml to confirm it's Snowflake-native (no password, no env_var)
3. Deploy the project to my schema using: snow dbt deploy HIIVE_MARKETPLACE --source @DATA/dbt_project --database HIIVE_COCO_HOL --schema <YOUR_USERNAME>_OPS
4. Verify the deployment by listing dbt projects in my schema

Execute everything and confirm the project is deployed."""

    render_prompt("Prompt 8a.1", "Migrate & Deploy from Stage", PROMPT_8A_1)

    render_explanation("What Prompt 8a.1 does", """
Copies the pre-built dbt project from the shared stage and deploys it as a native Snowflake object:

```bash
# Copy files to your personal stage
COPY FILES INTO @DATA/dbt_project/
  FROM @HIIVE_COCO_HOL.SHARED_DATA.WORKSHOP_FILES/dbt_project/;

# Deploy as a native dbt project object
snow dbt deploy HIIVE_MARKETPLACE \\
  --source @DATA/dbt_project \\
  --database HIIVE_COCO_HOL \\
  --schema <YOUR_USERNAME>_OPS
```

**What's different in profiles.yml?** The Snowflake-native version removes all authentication fields (password, private_key, env_var). When running inside Snowflake, the session already has credentials — no external auth needed.

**What `snow dbt deploy` does**: Packages all project files, uploads them to Snowflake, and creates a first-class dbt project object (VERSION$1). The project is now a Snowflake object you can DESCRIBE, ALTER, and EXECUTE — just like a table or view.
""")

    st.info("""
:material/visibility: **Verify in Snowsight**

Navigate to **Data → Databases → HIIVE_COCO_HOL → <YOUR_USERNAME>_OPS**. You should see a **dbt Project** object listed alongside your tables and views. Click it to view:
- Project metadata (name, creation time)
- VERSION$1 (the initial deployment)
- Source files included in the project
""")

    render_prompt("Prompt 8a.2", "Execute & Test", PROMPT_8_2)

    render_explanation("What Prompt 8a.2 does", """
Runs the deployed dbt project using native Snowflake compute:

```bash
snow dbt execute -c default \\
  --database HIIVE_COCO_HOL --schema <YOUR_USERNAME>_OPS \\
  HIIVE_MARKETPLACE build
```

This is equivalent to `dbt build` but runs entirely on Snowflake warehouse compute. No external runner, no GitHub Actions, no dbt Cloud.

**What `build` does**: Runs all models AND tests in dependency order. Staging models (views) are created first, then the mart table, then tests validate everything.

**Expected results**:
- 2 staging views created (STG_TRADES, STG_LISTINGS)
- 1 mart table created (MART_COMPANY_PERFORMANCE)
- Tests pass on primary keys (unique + not_null)

These are regular Snowflake objects — queryable by any tool, any role, any downstream process. No special dbt runtime needed to access them.
""")

    st.success("""
:material/table_chart: **Verify in Snowsight**

Navigate to your schema and verify the new objects:
- **STG_TRADES** (view) — Click → Data Preview to see cleaned trade data
- **STG_LISTINGS** (view) — Click → Data Preview to see listings with is_active flag
- **MART_COMPANY_PERFORMANCE** (table) — Click → Data Preview to see aggregated company metrics

These are regular Snowflake objects — queryable by any tool, dashboard, or downstream process. No special dbt runtime needed to access them.
""")

    render_prompt("Prompt 8a.3", "Schedule (Replace GitHub Actions)", PROMPT_8_3)

    render_explanation("What Prompt 8a.3 does", """
Creates a Snowflake Task that replaces the entire GitHub Actions workflow:

```sql
CREATE OR REPLACE TASK DBT_HOURLY_BUILD
  WAREHOUSE = HIIVE_COCO_HOL_WH
  SCHEDULE = 'USING CRON 0 * * * * America/Vancouver'
AS
  EXECUTE DBT PROJECT HIIVE_COCO_HOL.<YOUR_USERNAME>_OPS.HIIVE_MARKETPLACE
    ARGS = 'build';

ALTER TASK DBT_HOURLY_BUILD RESUME;
```

**One SQL statement replaces**:
- `.github/workflows/dbt.yml` (workflow definition)
- GitHub Actions CRON trigger
- Runner provisioning
- dbt CLI installation step
- `dbt run` / `dbt test` commands
- GitHub Secrets for Snowflake credentials

**Why this is better**: No external dependencies. No GitHub outages affecting your data pipeline. No credential rotation across systems. The task runs on Snowflake compute with native auth.
""")

    st.info("""
:material/schedule: **Verify in Snowsight**

Navigate to **Monitoring → Task History** in the left sidebar. You'll see your `DBT_HOURLY_BUILD` task with:
- **Schedule**: The CRON expression (every hour)
- **Status**: STARTED (active)
- **Execution history**: Each run shows duration, status, and error details

This replaces checking GitHub Actions logs entirely. All monitoring is inside Snowflake.
""")

    render_prompt("Prompt 8a.4", "Monitor & Debug", PROMPT_8_4)

    render_explanation("What Prompt 8a.4 does", """
Shows how to monitor and debug dbt projects without leaving Snowflake:

```sql
-- View all deployed versions
SHOW VERSIONS IN DBT PROJECT HIIVE_COCO_HOL.<YOUR_USERNAME>_OPS.HIIVE_MARKETPLACE;

-- Check task execution history
SELECT *
FROM TABLE(INFORMATION_SCHEMA.TASK_HISTORY(
  TASK_NAME => 'DBT_HOURLY_BUILD',
  RESULT_LIMIT => 10
));

-- Describe project metadata
DESCRIBE DBT PROJECT HIIVE_COCO_HOL.<YOUR_USERNAME>_OPS.HIIVE_MARKETPLACE;
```

**Versioned deployments**: Each `snow dbt deploy` creates VERSION$1, VERSION$2, etc. If a bad deploy goes out, rollback is one command — no git revert, no waiting for CI to re-run.

**Compared to GitHub Actions monitoring**:
- No switching between Snowsight and GitHub UI
- No scrolling through CI logs to find the failure
- Task history shows duration, status, and errors in one view
- Version history gives instant rollback without touching git
""")

    st.info("""
:material/history: **Verify in Snowsight**

Navigate to your dbt project object → **Versions** tab to see deployment history. Each `snow dbt deploy` creates a new version (VERSION$1, VERSION$2, ...) — giving you instant rollback capability without reverting git commits.

Compare this to GitHub Actions: if a bad deploy goes out, you'd need to revert the commit, wait for CI to re-run, and hope it passes. With native dbt, rollback is one SQL command:
```sql
ALTER DBT PROJECT HIIVE_MARKETPLACE SET DEFAULT_VERSION = 'VERSION$1';
```
""")


with tab_b:
    st.caption("Have Cortex Code generate the dbt project from scratch based on your schema.")

    PROMPT_8B_1 = """I want to create a dbt project that transforms my raw HIIVE marketplace tables into analytics-ready models, then deploy it natively to Snowflake.

Generate a dbt project called HIIVE_MARKETPLACE with:
- A Snowflake-native profiles.yml (no password, no env_var — auth is handled by the Snowflake session)
- Staging models: stg_trades (clean TRADE_EXECUTIONS) and stg_listings (clean LISTINGS with is_active flag)
- A mart model: mart_company_performance (joins companies + trades + listings, aggregates total volume, avg price, trade count, listing fill rate per company)
- A schema.yml with sources pointing to my raw tables, and tests (unique + not_null on primary keys)
- Staging models materialized as views, mart as a table

Then deploy it to my schema using snow dbt deploy.

Create all files, deploy, and verify the project exists in Snowflake."""

    render_prompt("Prompt 8b.1", "Generate & Deploy with CoCo", PROMPT_8B_1)

    render_explanation("What Prompt 8b.1 does", """
Has Cortex Code generate an entire dbt project from scratch and deploy it natively:

**Generated project structure**:
```
dbt_project/
├── dbt_project.yml
├── profiles.yml          # No password — Snowflake session auth
├── models/
│   ├── staging/
│   │   ├── stg_trades.sql
│   │   └── stg_listings.sql
│   ├── marts/
│   │   └── mart_company_performance.sql
│   └── schema.yml        # Sources, tests, docs
```

**profiles.yml (Snowflake-native)**:
```yaml
hiive_marketplace:
  target: default
  outputs:
    default:
      type: snowflake
      account: "{{ env_var('SNOWFLAKE_ACCOUNT') }}"
      database: HIIVE_COCO_HOL
      schema: <YOUR_USERNAME>_OPS
      # No password, no private_key — session auth handles it
```

**Why Option B?** CoCo reads your actual schema and generates models that match your real tables. If your tables have different columns than expected, CoCo adapts. Option A uses pre-built files that assume a specific schema.
""")

    st.info("""
:material/visibility: **Verify in Snowsight**

Navigate to **Data → Databases → HIIVE_COCO_HOL → <YOUR_USERNAME>_OPS**. You should see a **dbt Project** object listed alongside your tables and views. Click it to view:
- Project metadata (name, creation time)
- VERSION$1 (the initial deployment)
- Source files included in the project
""")

    render_prompt("Prompt 8b.2", "Execute & Test", PROMPT_8_2)

    render_explanation("What Prompt 8b.2 does", """
Runs the deployed dbt project using native Snowflake compute:

```bash
snow dbt execute -c default \\
  --database HIIVE_COCO_HOL --schema <YOUR_USERNAME>_OPS \\
  HIIVE_MARKETPLACE build
```

This is equivalent to `dbt build` but runs entirely on Snowflake warehouse compute. No external runner, no GitHub Actions, no dbt Cloud.

**What `build` does**: Runs all models AND tests in dependency order. Staging models (views) are created first, then the mart table, then tests validate everything.

**Expected results**:
- 2 staging views created (STG_TRADES, STG_LISTINGS)
- 1 mart table created (MART_COMPANY_PERFORMANCE)
- Tests pass on primary keys (unique + not_null)

These are regular Snowflake objects — queryable by any tool, any role, any downstream process. No special dbt runtime needed to access them.
""")

    st.success("""
:material/table_chart: **Verify in Snowsight**

Navigate to your schema and verify the new objects:
- **STG_TRADES** (view) — Click → Data Preview to see cleaned trade data
- **STG_LISTINGS** (view) — Click → Data Preview to see listings with is_active flag
- **MART_COMPANY_PERFORMANCE** (table) — Click → Data Preview to see aggregated company metrics

These are regular Snowflake objects — queryable by any tool, dashboard, or downstream process. No special dbt runtime needed to access them.
""")

    render_prompt("Prompt 8b.3", "Schedule (Replace GitHub Actions)", PROMPT_8_3)

    render_explanation("What Prompt 8b.3 does", """
Creates a Snowflake Task that replaces the entire GitHub Actions workflow:

```sql
CREATE OR REPLACE TASK DBT_HOURLY_BUILD
  WAREHOUSE = HIIVE_COCO_HOL_WH
  SCHEDULE = 'USING CRON 0 * * * * America/Vancouver'
AS
  EXECUTE DBT PROJECT HIIVE_COCO_HOL.<YOUR_USERNAME>_OPS.HIIVE_MARKETPLACE
    ARGS = 'build';

ALTER TASK DBT_HOURLY_BUILD RESUME;
```

**One SQL statement replaces**:
- `.github/workflows/dbt.yml` (workflow definition)
- GitHub Actions CRON trigger
- Runner provisioning
- dbt CLI installation step
- `dbt run` / `dbt test` commands
- GitHub Secrets for Snowflake credentials

**Why this is better**: No external dependencies. No GitHub outages affecting your data pipeline. No credential rotation across systems. The task runs on Snowflake compute with native auth.
""")

    st.info("""
:material/schedule: **Verify in Snowsight**

Navigate to **Monitoring → Task History** in the left sidebar. You'll see your `DBT_HOURLY_BUILD` task with:
- **Schedule**: The CRON expression (every hour)
- **Status**: STARTED (active)
- **Execution history**: Each run shows duration, status, and error details

This replaces checking GitHub Actions logs entirely. All monitoring is inside Snowflake.
""")

    render_prompt("Prompt 8b.4", "Monitor & Debug", PROMPT_8_4)

    render_explanation("What Prompt 8b.4 does", """
Shows how to monitor and debug dbt projects without leaving Snowflake:

```sql
-- View all deployed versions
SHOW VERSIONS IN DBT PROJECT HIIVE_COCO_HOL.<YOUR_USERNAME>_OPS.HIIVE_MARKETPLACE;

-- Check task execution history
SELECT *
FROM TABLE(INFORMATION_SCHEMA.TASK_HISTORY(
  TASK_NAME => 'DBT_HOURLY_BUILD',
  RESULT_LIMIT => 10
));

-- Describe project metadata
DESCRIBE DBT PROJECT HIIVE_COCO_HOL.<YOUR_USERNAME>_OPS.HIIVE_MARKETPLACE;
```

**Versioned deployments**: Each `snow dbt deploy` creates VERSION$1, VERSION$2, etc. If a bad deploy goes out, rollback is one command — no git revert, no waiting for CI to re-run.

**Compared to GitHub Actions monitoring**:
- No switching between Snowsight and GitHub UI
- No scrolling through CI logs to find the failure
- Task history shows duration, status, and errors in one view
- Version history gives instant rollback without touching git
""")

    st.info("""
:material/history: **Verify in Snowsight**

Navigate to your dbt project object → **Versions** tab to see deployment history. Each `snow dbt deploy` creates a new version (VERSION$1, VERSION$2, ...) — giving you instant rollback capability without reverting git commits.

Compare this to GitHub Actions: if a bad deploy goes out, you'd need to revert the commit, wait for CI to re-run, and hope it passes. With native dbt, rollback is one SQL command:
```sql
ALTER DBT PROJECT HIIVE_MARKETPLACE SET DEFAULT_VERSION = 'VERSION$1';
```
""")


render_key_concepts([
    {"term": "Migration Path", "definition": "What changes: profiles.yml (remove auth fields), dbt_project.yml (replace env_var with literals). What stays: ALL SQL models, tests, schema.yml — zero modifications needed. The entire transformation logic is portable as-is."},
    {"term": "EXECUTE DBT PROJECT", "definition": "Native SQL command that runs dbt on Snowflake warehouse compute. Supports build, run, test, and seed. No external runner or CI system needed. The warehouse handles compute, and the session handles auth."},
    {"term": "Versioned Deployments", "definition": "Each `snow dbt deploy` creates VERSION$1, $2, etc. Rollback = change default version with one ALTER statement. No git revert needed, no waiting for CI to re-run. Instant rollback with audit trail."},
    {"term": "Snowflake Task Scheduling", "definition": "Same Task infrastructure used elsewhere in Snowflake (Dynamic Tables, Streams, etc.). Replaces GitHub Actions CRON triggers entirely. One SQL statement replaces an entire workflow YAML file plus runner infrastructure."},
    {"term": "dbt show (Preview)", "definition": "Native command that previews model output WITHOUT materializing any objects. Impossible with standard dbt run — you always have to create/replace tables to see results. A key differentiator for development and validation workflows."},
    {"term": "Task Chains", "definition": "Snowflake Tasks with AFTER dependencies create execution DAGs. Run → test → notify mirrors GitHub Actions step sequencing but with native guarantees, no external dependencies, and unified monitoring."},
])

render_docs_links([
    {"title": "dbt Projects on Snowflake", "url": "https://docs.snowflake.com/en/developer-guide/dbt/dbt-snowflake"},
    {"title": "snow dbt deploy", "url": "https://docs.snowflake.com/en/developer-guide/snowflake-cli/dbt/overview"},
    {"title": "EXECUTE DBT PROJECT", "url": "https://docs.snowflake.com/en/sql-reference/sql/execute-dbt-project"},
    {"title": "Snowflake Tasks", "url": "https://docs.snowflake.com/en/user-guide/tasks-intro"},
])

render_what_you_built([
    "HIIVE_MARKETPLACE dbt project deployed natively to Snowflake",
    "3 dbt models materialized (2 staging views, 1 mart table)",
    "DBT_HOURLY_BUILD Snowflake Task replacing GitHub Actions",
    "Monitoring queries for execution history and project versions",
    "Production task chain (run \u2192 test) with AFTER dependency",
    "Versioned deployment with instant rollback capability",
])

render_what_you_built([
    "HIIVE_MARKETPLACE dbt project deployed natively to Snowflake",
    "3 dbt models materialized (2 staging views, 1 mart table)",
    "DBT_HOURLY_BUILD Snowflake Task replacing GitHub Actions",
    "Monitoring queries for execution history and project versions",
])
