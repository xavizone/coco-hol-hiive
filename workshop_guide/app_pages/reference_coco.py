import streamlit as st

st.title("Reference: Cortex Code Plugin for Claude")
st.markdown("Extend your existing Claude Code workflow with native Snowflake context")

st.space("small")

st.markdown("#### Why CoCo for HIIVE")
with st.container(border=True):
    st.markdown("""
You already use Claude Code daily with custom skills. **Cortex Code (CoCo)** adds Snowflake-native context:

- **Schema awareness** — CoCo knows your tables, columns, and types without you describing them
- **Semantic view discovery** — iterate on semantic views with instant validation
- **Query execution** — write and run SQL in one place, no copy-pasting to Snowsight
- **DDL generation** — create objects with full context of what already exists

It collapses the distance between AI assistance and Snowflake execution.
""")

st.space("small")

st.markdown("#### Installation")
with st.container(border=True):
    st.markdown("""
1. Open **VS Code** (where you already have Claude Code installed)
2. Extensions marketplace → search **"Snowflake"** → Install the **Snowflake** extension
3. The Cortex Code assistant is part of the Snowflake extension
4. Sign in: Command Palette (`Cmd+Shift+P`) → **"Snowflake: Sign In"** → use your Snowflake credentials
5. Verify: you should see the Snowflake sidebar with your databases listed
""")

st.space("small")

st.markdown("#### Connecting to Your Account")
with st.container(border=True):
    st.markdown("Connection config lives in VS Code settings or `~/.snowflake/connections.toml`:")
    st.code("""[hiive_coco_hol]
account = "your_account"
user = "your_user"
authenticator = "externalbrowser"
warehouse = "HIIVE_COCO_HOL_WH"
database = "HIIVE_COCO_HOL"
schema = ""  # Leave blank - set per session
""", language="toml")
    st.markdown("""
:material/warning: **Cloudflare VPN note**: If you're behind Cloudflare VPN and see SSL certificate errors, add `insecure_mode = true` under your connection block in `~/.snowflake/connections.toml`:

```toml
[default]
insecure_mode = true
```

This disables certificate verification for that connection. Remove it once you're off the VPN or the cert issue is resolved.
""")

st.space("small")

st.markdown("#### Key Workflows")
st.markdown("Examples of what CoCo can do that generic Claude Code cannot:")

col1, col2 = st.columns(2)

with col1:
    with st.container(border=True):
        st.markdown(":material/database: **Schema Discovery**")
        st.caption("\"Show me all tables in HIIVE_COCO_HOL.<username>_OPS and their row counts\"")
        st.markdown("CoCo executes this against live Snowflake — no manual connection setup.")

    with st.container(border=True):
        st.markdown(":material/chat: **Semantic View Iteration**")
        st.caption("\"Add a metric to MARKETPLACE_ANALYTICS_VIEW that calculates average days from listing to trade execution\"")
        st.markdown("CoCo knows the semantic view DDL syntax and validates inline.")

    with st.container(border=True):
        st.markdown(":material/edit: **Query Authoring with Context**")
        st.caption("\"Write a query showing top 10 companies by month-over-month trade volume growth\"")
        st.markdown("CoCo auto-discovers column names and types from your schema.")

with col2:
    with st.container(border=True):
        st.markdown(":material/monitoring: **DMF Management**")
        st.caption("\"Show me all DMF results from the last 24 hours where anomalies were detected\"")
        st.markdown("CoCo runs the query and shows results inline — no context switching.")

    with st.container(border=True):
        st.markdown(":material/code: **dbt Integration**")
        st.caption("\"Read my dbt model for trade_executions and suggest a test for NULL compliance_status\"")
        st.markdown("CoCo can read your dbt models, understand refs, and suggest changes in context.")

    with st.container(border=True):
        st.markdown(":material/terminal: **DDL Generation**")
        st.caption("\"Create a new table for tracking 409A valuation history with appropriate constraints\"")
        st.markdown("CoCo generates DDL aware of your existing schema and naming conventions.")

st.space("small")

st.markdown("#### CoCo vs Claude Code — When to Use Which")
with st.container(border=True):
    st.markdown("""
| Scenario | Use CoCo | Use Claude Code |
|----------|:--------:|:---------------:|
| Write/debug SQL against Snowflake | :white_check_mark: | |
| Create/modify Snowflake objects | :white_check_mark: | |
| Semantic view development | :white_check_mark: | |
| DMF creation and monitoring | :white_check_mark: | |
| dbt model Python/Jinja logic | | :white_check_mark: |
| Git operations, PRs, code review | | :white_check_mark: |
| General Python/TypeScript development | | :white_check_mark: |
| dbt SQL that targets Snowflake | :white_check_mark: (validation) | :white_check_mark: (editing) |
""")

st.space("small")

st.markdown("#### Tips for Your Team")
with st.container(border=True):
    st.markdown("""
- **Oleg / Abhi**: Use CoCo for semantic view iteration — faster feedback loop than the Snowsight sidebar
- **Lauren / Fernando**: Use CoCo for DMF creation and monitoring queries — write and execute in one place
- **Everyone**: CoCo can discover existing tables/views, so you don't need to remember exact schema names
- **Workflow**: Use Claude Code for dbt model logic → switch to CoCo to validate the compiled SQL runs correctly
""")
