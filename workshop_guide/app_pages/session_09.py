import streamlit as st
from components import render_session_header, render_explanation, render_technologies_used, render_key_concepts, render_what_you_built

render_session_header(9, "dbt Projects (Hands-On)", "11:45 AM - 12:05 PM", "20 min", "Deploy, execute, version, and schedule a dbt project natively in Snowflake using SQL and CLI")

render_technologies_used([
    {"name": "snow dbt deploy", "description": "Snowflake CLI command that packages a local dbt project and uploads it as a first-class Snowflake object. Creates versioned deployments with instant rollback.", "icon": "cloud_upload"},
    {"name": "EXECUTE DBT PROJECT", "description": "Native SQL command that runs dbt (build, run, test, show) directly on Snowflake warehouse compute. No external runner or CI system needed.", "icon": "play_circle"},
    {"name": "Snowflake Tasks", "description": "CRON-based scheduling with AFTER dependencies. Replaces GitHub Actions entirely — one SQL statement per pipeline step.", "icon": "schedule"},
])

st.info("""
:material/swap_horiz: **What this session demonstrates**

This session uses **SQL commands and the Snowflake CLI** (not Cortex Code prompts) to show how your team would migrate an existing dbt project from GitHub Actions to Snowflake-native execution.

**What changes**: `profiles.yml` (remove auth fields) — that's it.
**What stays the same**: All SQL models, tests, schema.yml — zero modifications.

| Current State | Native Snowflake |
|--------------|------------------|
| GitHub repo → GH Actions → external runner → `dbt run` | `snow dbt deploy` → `EXECUTE DBT PROJECT` on Snowflake compute |
| Scheduling via GH Actions YAML | Snowflake Task (1 SQL statement) |
| Debugging via GitHub Actions logs | Query task history directly in Snowflake |
| Rollback = revert commit + wait for CI | `ALTER ... SET DEFAULT_VERSION` (instant) |
""")

st.markdown("---")

# ─────────────────────────────────────────────────────────────────────────────
# Step 1: Deploy from Git
# ─────────────────────────────────────────────────────────────────────────────

st.markdown("### Step 1: Deploy Your dbt Project to Snowflake")

with st.container(border=True):
    st.markdown("""
**Prerequisites**: You have the `snow` CLI installed (`brew install snowflake-cli`) and a connection configured in `~/.snowflake/connections.toml`.

**1a. Clone the project** (or use your existing dbt project):
""")
    st.code("""git clone https://github.com/xavizone/coco-hol-hiive.git
cd coco-hol-hiive/workshop_guide/dbt_project""", language="bash")

    st.markdown("""
**1b. Review and update `profiles.yml`** for Snowflake-native execution:
""")

    col1, col2 = st.columns(2)
    with col1:
        st.markdown("**Before** (GitHub Actions auth):")
        st.code("""default:
  outputs:
    dev:
      type: snowflake
      account: "{{ env_var('SNOWFLAKE_ACCOUNT') }}"
      user: "{{ env_var('SNOWFLAKE_USER') }}"
      password: "{{ env_var('SNOWFLAKE_PASSWORD') }}"
      role: HIIVE_COCO_HOL_ROLE
      warehouse: HIIVE_COCO_HOL_WH
      database: HIIVE_COCO_HOL""", language="yaml")

    with col2:
        st.markdown("**After** (Snowflake-native):")
        st.code("""default:
  target: dev
  outputs:
    dev:
      type: snowflake
      account: "your_account"
      role: HIIVE_COCO_HOL_ROLE
      warehouse: HIIVE_COCO_HOL_WH
      database: HIIVE_COCO_HOL
      schema: "{{ target.schema }}"
      threads: 4""", language="yaml")

    st.caption("Remove `password`, `user`, and any `env_var()` calls. Snowflake session auth handles credentials automatically.")

    st.markdown("**1c. Deploy** to your schema:")
    st.code("""snow dbt deploy HIIVE_MARKETPLACE \\
  --source ./workshop_guide/dbt_project \\
  --database HIIVE_COCO_HOL \\
  --schema <YOUR_USERNAME>_OPS""", language="bash")

render_explanation("What `snow dbt deploy` does", """
Packages all project files (models, tests, profiles.yml, dbt_project.yml) and creates a **dbt Project object** in Snowflake — a first-class versioned object like a table or view.

- Creates `VERSION$1` on first deploy
- Subsequent deploys create `VERSION$2`, `VERSION$3`, etc.
- Each version is a complete snapshot of the project at deploy time
- Your SQL model files are stored byte-for-byte unchanged inside Snowflake
""")

st.info("""
:material/visibility: **Verify in Snowsight**

Navigate to **Data → Databases → HIIVE_COCO_HOL → <your_schema>**. You should see a **dbt Project** object (HIIVE_MARKETPLACE) listed alongside your tables and views.

Click it to view:
- **Overview**: Project name, creation time, default version
- **Versions** tab: VERSION$1 with timestamp
- **Files** tab: Your actual model SQL files stored in Snowflake
""")

# ─────────────────────────────────────────────────────────────────────────────
# Step 2: Verify Deployment
# ─────────────────────────────────────────────────────────────────────────────

st.markdown("### Step 2: Verify the Deployment")

with st.container(border=True):
    st.markdown("Run these SQL commands to confirm the project was deployed correctly:")
    st.code("""-- List all dbt projects in your schema
SHOW DBT PROJECTS IN SCHEMA HIIVE_COCO_HOL.<YOUR_USERNAME>_OPS;

-- Check the version that was created
SHOW VERSIONS IN DBT PROJECT HIIVE_COCO_HOL.<YOUR_USERNAME>_OPS.HIIVE_MARKETPLACE;

-- Inspect project metadata
DESCRIBE DBT PROJECT HIIVE_COCO_HOL.<YOUR_USERNAME>_OPS.HIIVE_MARKETPLACE;""", language="sql")

    st.markdown("**Or via CLI:**")
    st.code("""snow dbt list --database HIIVE_COCO_HOL --in schema <YOUR_USERNAME>_OPS""", language="bash")

render_explanation("What each verification confirms", """
| Command | What it tells you |
|---------|-------------------|
| `SHOW DBT PROJECTS` | Project exists in your schema |
| `SHOW VERSIONS` | VERSION$1 was created with timestamp |
| `DESCRIBE DBT PROJECT` | Project metadata: name, database, schema, default version, comment |
| `snow dbt list` | CLI-friendly list of all projects in the schema |
""")

# ─────────────────────────────────────────────────────────────────────────────
# Step 3: Execute Common dbt Tasks
# ─────────────────────────────────────────────────────────────────────────────

st.markdown("### Step 3: Execute dbt Tasks Natively")

with st.container(border=True):
    st.markdown("Run each command to see the native dbt workflow in action:")

    st.markdown("**3a. List all project resources:**")
    st.code("""snow dbt execute -c default --database HIIVE_COCO_HOL \\
  --schema <YOUR_USERNAME>_OPS HIIVE_MARKETPLACE list""", language="bash")

    st.markdown("**3b. Preview a model WITHOUT materializing** (the `show` command):")
    st.code("""snow dbt execute -c default --database HIIVE_COCO_HOL \\
  --schema <YOUR_USERNAME>_OPS HIIVE_MARKETPLACE show \\
  --select mart_company_performance""", language="bash")
    st.caption("This returns rows the model WOULD produce — without creating any objects. A key differentiator.")

    st.markdown("**3c. Run the full build** (models + tests in dependency order):")
    st.code("""snow dbt execute -c default --database HIIVE_COCO_HOL \\
  --schema <YOUR_USERNAME>_OPS HIIVE_MARKETPLACE build""", language="bash")

    st.markdown("**3d. Run tests only** (validate data quality on existing objects):")
    st.code("""snow dbt execute -c default --database HIIVE_COCO_HOL \\
  --schema <YOUR_USERNAME>_OPS HIIVE_MARKETPLACE test""", language="bash")

    st.markdown("**3e. Run specific models only:**")
    st.code("""snow dbt execute -c default --database HIIVE_COCO_HOL \\
  --schema <YOUR_USERNAME>_OPS HIIVE_MARKETPLACE run \\
  --select stg_trades stg_listings""", language="bash")

render_explanation("Differentiators vs GitHub Actions", """
| Capability | GitHub Actions | Snowflake Native |
|-----------|---------------|------------------|
| **Preview without materializing** | Not possible — must run full pipeline | `show` command returns rows instantly |
| **Selective model runs** | Modify workflow YAML or use tags | `--select` flag on any execution |
| **Test independently** | Coupled to full `dbt build` in CI | Run `test` anytime on existing objects |
| **Time to first result** | Clone → install deps → configure → run | One command, instant |
| **Where it runs** | External GitHub runner (your compute $$) | Snowflake warehouse (existing infra) |
""")

st.success("""
:material/table_chart: **Verify in Snowsight**

Navigate to your schema and confirm the new objects:
- **STG_TRADES** (view) — Click → Data Preview to see cleaned trade data
- **STG_LISTINGS** (view) — Click → Data Preview to see listings with is_active flag
- **MART_COMPANY_PERFORMANCE** (table) — Click → Data Preview to see aggregated company metrics

These are regular Snowflake objects — queryable by any tool, dashboard, or role.
""")

# ─────────────────────────────────────────────────────────────────────────────
# Step 4: Version Management & Rollback
# ─────────────────────────────────────────────────────────────────────────────

st.markdown("### Step 4: Update, Version & Rollback")

with st.container(border=True):
    st.markdown("""
**4a. Make a change** to a model locally (e.g., add `avg_commission` column to the mart), then re-deploy:
""")
    st.code("""snow dbt deploy HIIVE_MARKETPLACE \\
  --source ./workshop_guide/dbt_project \\
  --database HIIVE_COCO_HOL \\
  --schema <YOUR_USERNAME>_OPS""", language="bash")
    st.caption("Same command as before — Snowflake automatically creates VERSION$2.")

    st.markdown("**4b. Verify both versions exist:**")
    st.code("""SHOW VERSIONS IN DBT PROJECT HIIVE_COCO_HOL.<YOUR_USERNAME>_OPS.HIIVE_MARKETPLACE;""", language="sql")

    st.markdown("**4c. Execute the updated version** with `--full-refresh` for schema changes:")
    st.code("""snow dbt execute -c default --database HIIVE_COCO_HOL \\
  --schema <YOUR_USERNAME>_OPS HIIVE_MARKETPLACE run \\
  --full-refresh --select mart_company_performance""", language="bash")

    st.markdown("**4d. Rollback** if something goes wrong (instant — 1 second):")
    st.code("""ALTER DBT PROJECT HIIVE_COCO_HOL.<YOUR_USERNAME>_OPS.HIIVE_MARKETPLACE
  SET DEFAULT_VERSION = 'VERSION$1';""", language="sql")

render_explanation("Why this is better than git-based rollback", """
| Scenario | GitHub Actions | Snowflake Native |
|----------|---------------|------------------|
| **Bad deploy discovered** | Revert commit → push → wait for CI (5-15 min) | One ALTER statement (1 second) |
| **Audit trail** | Git log (code only) | Snowflake versions (code + deployment metadata + timestamp) |
| **Partial rollback** | Not easily possible | Roll back project version while keeping data |
| **Preview before promoting** | Run full CI on a branch | `show` command on any version |
""")

st.info("""
:material/history: **Verify in Snowsight**

Navigate to your dbt project → **Versions** tab:
- **VERSION$1** — Original deployment
- **VERSION$2** — Updated version

The default version indicator shows which is active. After rollback, VERSION$1 is the active default.
""")

# ─────────────────────────────────────────────────────────────────────────────
# Step 5: Schedule with Task Chain
# ─────────────────────────────────────────────────────────────────────────────

st.markdown("### Step 5: Schedule with a Task Chain (Replace GitHub Actions)")

with st.container(border=True):
    st.markdown("Create a production-grade task chain that replaces your `.github/workflows/dbt.yml`:")
    st.code("""-- Root task: run models on schedule
CREATE OR REPLACE TASK HIIVE_COCO_HOL.<YOUR_USERNAME>_OPS.DBT_SCHEDULED_RUN
  WAREHOUSE = HIIVE_COCO_HOL_WH
  SCHEDULE = 'USING CRON 0 * * * * America/Vancouver'
AS
  EXECUTE DBT PROJECT HIIVE_COCO_HOL.<YOUR_USERNAME>_OPS.HIIVE_MARKETPLACE
    ARGS = 'run';

-- Dependent task: test AFTER models complete
CREATE OR REPLACE TASK HIIVE_COCO_HOL.<YOUR_USERNAME>_OPS.DBT_SCHEDULED_TEST
  WAREHOUSE = HIIVE_COCO_HOL_WH
  AFTER HIIVE_COCO_HOL.<YOUR_USERNAME>_OPS.DBT_SCHEDULED_RUN
AS
  EXECUTE DBT PROJECT HIIVE_COCO_HOL.<YOUR_USERNAME>_OPS.HIIVE_MARKETPLACE
    ARGS = 'test';

-- Resume tasks (child first, then root)
ALTER TASK HIIVE_COCO_HOL.<YOUR_USERNAME>_OPS.DBT_SCHEDULED_TEST RESUME;
ALTER TASK HIIVE_COCO_HOL.<YOUR_USERNAME>_OPS.DBT_SCHEDULED_RUN RESUME;

-- Verify
SHOW TASKS IN SCHEMA HIIVE_COCO_HOL.<YOUR_USERNAME>_OPS;""", language="sql")

render_explanation("Direct mapping to GitHub Actions", """
| GitHub Actions (.yml) | Snowflake Task (SQL) |
|----------------------|---------------------|
| `on: schedule: cron: '0 * * * *'` | `SCHEDULE = 'USING CRON 0 * * * *'` |
| `jobs: build: steps: - run: dbt run` | `EXECUTE DBT PROJECT ... ARGS = 'run'` |
| `jobs: test: needs: [build]` | `AFTER DBT_SCHEDULED_RUN` |
| `env: SNOWFLAKE_PASSWORD: ${{ secrets.SF_PASS }}` | Session auth — no secrets needed |
| GitHub-hosted runner provisioning | Warehouse auto-resumes (already exists) |
| Failure notification via Slack action | Snowflake Alert on task failure |

**What you eliminate:**
- `.github/workflows/dbt.yml` (entire file)
- GitHub Secrets configuration and rotation
- Runner provisioning and cost
- External dependency on GitHub's uptime
- Debugging across two systems (GitHub UI + Snowflake)
""")

st.info("""
:material/schedule: **Verify in Snowsight**

Navigate to **Monitoring → Task History**:
- **DBT_SCHEDULED_RUN** — Root task with hourly CRON
- **DBT_SCHEDULED_TEST** — Dependent task (runs after models)

Click either task to see:
- Dependency graph (visualized as a DAG)
- Execution history with duration and status
- Error details if a run failed

This single view replaces checking GitHub Actions logs.
""")

# ─────────────────────────────────────────────────────────────────────────────
# Key Concepts & Summary
# ─────────────────────────────────────────────────────────────────────────────

render_key_concepts([
    {"term": "Migration Path", "definition": "Remove auth fields from profiles.yml (password, env_var). Replace env_var() with literal values. All SQL models, tests, and schema.yml stay byte-for-byte unchanged."},
    {"term": "snow dbt deploy", "definition": "CLI command that packages a local dbt project directory and creates a versioned Snowflake object. Each deploy creates a new version (VERSION$1, $2, etc.) with instant rollback via ALTER."},
    {"term": "EXECUTE DBT PROJECT", "definition": "Native SQL command that runs dbt on Snowflake warehouse compute. Supports: run, build, test, seed, show (preview), list. No external runner, no dbt CLI installation needed."},
    {"term": "dbt show (Preview)", "definition": "Previews model output WITHOUT materializing objects. Returns rows the model would produce. Impossible with dbt run — a key differentiator for development and validation."},
    {"term": "Versioned Deployments", "definition": "Each deploy creates VERSION$N. Rollback = ALTER ... SET DEFAULT_VERSION (instant). No git revert, no CI re-run. Full audit trail with timestamps."},
    {"term": "Task Chains (AFTER)", "definition": "Tasks with AFTER dependencies form execution DAGs. Run → test → notify mirrors CI steps but with Snowflake SLA, native auth, and unified monitoring."},
])

render_what_you_built([
    "HIIVE_MARKETPLACE dbt project deployed as a Snowflake object",
    "Verified deployment with SHOW/DESCRIBE commands",
    "Executed native dbt tasks: list, show (preview), build, test, run --select",
    "Created VERSION$2 and demonstrated instant rollback",
    "Production task chain (run → test) replacing GitHub Actions",
])
