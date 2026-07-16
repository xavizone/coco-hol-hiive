import streamlit as st

st.title("Reference: Cortex Code")
st.markdown("Snowflake's AI coding assistant — available in Snowsight and VS Code")

st.space("small")

st.markdown("#### What is Cortex Code")
with st.container(border=True):
    st.markdown("""
**Cortex Code (CoCo)** is Snowflake's built-in AI assistant that understands your data platform natively:

- **Schema awareness** — knows your tables, columns, types, and relationships without you describing them
- **Semantic view discovery** — iterates on semantic views with instant validation
- **Query execution** — writes and runs SQL in one place, no copy-pasting between tools
- **Object creation** — generates DDL with full context of what already exists
- **dbt integration** — deploys and executes dbt projects natively

It's available in two places:
1. **Snowsight** — built into the Snowflake web UI (used for Sessions 1-7)
2. **VS Code** — via the Snowflake extension (used for Sessions 8-9 and daily workflow)
""")

st.space("small")

st.markdown("#### Installation (VS Code)")
with st.container(border=True):
    st.markdown("""
1. Open **VS Code**
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
st.markdown("Examples of what Cortex Code can do with native Snowflake context:")

col1, col2 = st.columns(2)

with col1:
    with st.container(border=True):
        st.markdown(":material/database: **Schema Discovery**")
        st.caption("\"Show me all tables in my schema and their row counts\"")
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
        st.markdown(":material/transform: **dbt Integration**")
        st.caption("\"Deploy my dbt project and run a full build with tests\"")
        st.markdown("CoCo executes `snow dbt deploy` and `EXECUTE DBT PROJECT` natively.")

    with st.container(border=True):
        st.markdown(":material/terminal: **DDL Generation**")
        st.caption("\"Create a Cortex Agent with Analyst and Search tools for our marketplace data\"")
        st.markdown("CoCo generates DDL aware of your existing schema and naming conventions.")

st.space("small")

st.markdown("#### Snowsight CoCo vs VS Code CoCo")
with st.container(border=True):
    st.markdown("""
| Capability | Snowsight CoCo | VS Code CoCo |
|-----------|:--------------:|:------------:|
| SQL execution and results | :white_check_mark: | :white_check_mark: |
| Semantic view creation | :white_check_mark: | :white_check_mark: |
| Cortex Agent creation | :white_check_mark: | :white_check_mark: |
| DMF creation and monitoring | :white_check_mark: | :white_check_mark: |
| Streamlit app development | :white_check_mark: (Workspaces editor) | :white_check_mark: (local + deploy) |
| dbt deploy via CLI | | :white_check_mark: |
| File editing and git integration | | :white_check_mark: |
| Multi-file project navigation | | :white_check_mark: |
| CoWork collaborative analysis | :white_check_mark: | |

**Recommendation**: Use **Snowsight CoCo** for quick SQL tasks, object creation, and exploration. Use **VS Code CoCo** for multi-file projects, dbt workflows, and daily development where you need terminal access.
""")

st.space("small")

st.markdown("#### Tips for Your Team")
with st.container(border=True):
    st.markdown("""
- **Data Engineers**: Use CoCo for DMF creation, dbt deployment, and pipeline monitoring — write and execute in one place
- **Analysts**: Use CoCo for semantic view iteration and ad-hoc SQL — faster feedback loop than the Snowsight sidebar
- **Platform Engineers**: Use CoCo for Cortex Agent and Search service setup — DDL generation with context
- **Everyone**: CoCo discovers existing tables/views automatically, so you don't need to remember exact schema names
- **Workflow**: Use VS Code CoCo for dbt model logic → deploy with `snow dbt deploy` → monitor with Snowsight CoCo
""")

st.space("small")

st.markdown("#### Documentation Links")
with st.container(border=True):
    st.markdown("""
- [Cortex Code in Snowsight](https://docs.snowflake.com/en/user-guide/ui-snowsight/cortex-code) — Getting started with the browser-based assistant
- [Snowflake Extension for VS Code](https://docs.snowflake.com/en/user-guide/vscode-ext) — Installation and configuration
- [Snowflake CLI](https://docs.snowflake.com/en/developer-guide/snowflake-cli/index) — CLI installation and connection setup
- [connections.toml Reference](https://docs.snowflake.com/en/developer-guide/snowflake-cli/connecting/specify-credentials) — Connection configuration options
""")
