import streamlit as st
from components import render_session_header, render_prompt, render_explanation, render_technologies_used, render_key_concepts, render_what_you_built

render_session_header(6, "Streamlit", "11:15 - 11:30 AM", "15 min", "Operations dashboard with AI chat interface")

render_technologies_used([
    {"name": "Streamlit in Snowflake (SiS)", "description": "Deploy Python-based data apps directly within Snowflake. Apps run on container runtime with full Python package support, access data natively via Snowpark, and inherit Snowflake's security model.", "icon": "web"},
    {"name": "Compute Pool", "description": "A managed pool of container nodes that powers SiS apps. Provides CPU/GPU resources, auto-scales, and supports any Python package from pip.", "icon": "memory"},
    {"name": "st.connection(\"snowflake\")", "description": "The Streamlit connection API for Snowflake on container runtime. Returns a connection object with .session() for Snowpark. No credentials needed — inherits the logged-in user's session.", "icon": "terminal"},
])

st.markdown("---")

st.markdown("#### :material/open_in_new: Open Workspaces")
with st.container(border=True):
    st.markdown("""
For this section, open **Workspaces** in Snowsight (left navigation panel → Projects → Workspaces). Workspaces provides an IDE-like environment where Cortex Code can create and edit Streamlit app files directly.

Paste the prompts below into Cortex Code **within Workspaces** so the generated code is written directly into your app files.
""")


PROMPT_6_1 = """In HIIVE_AI.MARKETPLACE_OPS, create a Streamlit app called MARKETPLACE_DASHBOARD that runs on the container runtime.

First, create a compute pool for the app:
- Name: HIIVE_COMPUTE_POOL
- Use the CPU_X64_S instance family
- Min and max nodes of 1

Then create the Streamlit app on that compute pool with these 2 pages:

PAGE 1 - Marketplace Dashboard:
- KPI cards at the top showing: Total Trade Volume USD (from TRADE_EXECUTIONS), Active Listings (count with status 'active' from LISTINGS), Avg Execution Price (from TRADE_EXECUTIONS), Compliance Clearance Rate (% with status 'cleared' from COMPLIANCE_REVIEWS)
- A bar chart of trade volume by company (join TRADE_EXECUTIONS to COMPANIES)
- A line chart showing daily trades over time
- A table of recent compliance reviews with risk_score color coding

PAGE 2 - Marketplace Intelligence Chat:
- A chat interface where users can type natural language questions
- Uses our MARKETPLACE_OPS_AGENT via SNOWFLAKE.CORTEX.AGENT() to answer questions
- Has a sidebar showing summary stats: total trades, active listings, companies tracked

Important for container runtime:
- Create an External Access Integration that allows access to pypi.org and files.pythonhosted.org
- Create a network rule for these hosts, then an integration referencing it
- Set EXTERNAL_ACCESS_INTEGRATIONS on the Streamlit app
- Include a pyproject.toml with dependencies: ["streamlit[snowflake]>=1.50.0", "plotly"]
- Use st.connection("snowflake") for the Snowflake connection
- Make it visually clean with st.columns for layout

Execute all SQL to create the compute pool, stage the files, and deploy the app."""

render_prompt("Prompt 6.1", "Create the Streamlit App", PROMPT_6_1)

render_explanation("What this prompt does", """
Creates a full **Streamlit in Snowflake** application on the **container runtime**:

**Step 1 — Compute pool**:
```sql
CREATE COMPUTE POOL HIIVE_COMPUTE_POOL
  MIN_NODES = 1 MAX_NODES = 1
  INSTANCE_FAMILY = CPU_X64_S;
```

**Step 2 — External Access Integration** (so container can install pip packages):
```sql
CREATE NETWORK RULE pypi_network_rule
  MODE = EGRESS TYPE = HOST_PORT
  VALUE_LIST = ('pypi.org', 'files.pythonhosted.org');

CREATE EXTERNAL ACCESS INTEGRATION pypi_access_integration
  ALLOWED_NETWORK_RULES = (pypi_network_rule) ENABLED = TRUE;
```

**Step 3 — Stage files and deploy**:
- Write streamlit_app.py, pages, and pyproject.toml to a stage
- Create the Streamlit object on the compute pool

**Page 1 — Marketplace Dashboard** pattern:
```python
conn = st.connection("snowflake")
session = conn.session()
volume_df = session.sql("SELECT SUM(trade_value) FROM TRADE_EXECUTIONS").collect()
st.metric("Total Trade Volume", f"${volume_df[0][0]:,.0f}")
```

**Page 2 — Chat interface** uses `st.chat_input` and `st.chat_message` with the MARKETPLACE_OPS_AGENT for responses.

**Key advantages of SiS**:
- **No data movement**: App runs inside Snowflake
- **Security**: Inherits user's role and permissions
- **No infrastructure**: Compute pool auto-manages lifecycle
""")


PROMPT_6_2 = """Show me the SQL to verify the Streamlit app and compute pool:

1. SHOW COMPUTE POOLS;
2. SHOW STREAMLITS IN SCHEMA HIIVE_AI.MARKETPLACE_OPS;
3. Describe the streamlit MARKETPLACE_DASHBOARD;

Also provide me with the direct URL to open the Streamlit app in Snowsight."""

render_prompt("Prompt 6.2", "Verify & Access the App", PROMPT_6_2)

st.success("""
:material/rocket_launch: **Preview and Deploy your app!**

Once Cortex Code has generated your app files in Workspaces:

1. **Run** — Click the **Run** button (▶️) in the top-right of the Workspaces editor to preview your app. This launches a local preview so you can see the dashboard and chat interface in action.

2. **Deploy** — When you're happy with the preview, click **Deploy** to publish the app to your Snowflake account. This makes it accessible to anyone with the appropriate role via Snowsight.

Try modifying the app (add a chart, change KPI labels) and re-run to see changes live!
""")

render_explanation("What this prompt does", """
Verification and access:

**SHOW COMPUTE POOLS** — confirms the pool is ACTIVE with correct instance family.

**SHOW STREAMLITS** — lists the app with its URL endpoint.

**DESCRIBE STREAMLIT** — shows main file, compute pool (confirms container runtime), and status.

**Accessing the app**: SiS apps are accessible via Snowsight at:
```
https://app.snowflake.com/<account>/#/streamlit-apps/HIIVE_AI.MARKETPLACE_OPS.MARKETPLACE_DASHBOARD
```

**Sharing the app** with other roles:
```sql
GRANT USAGE ON STREAMLIT MARKETPLACE_DASHBOARD TO ROLE <role_name>;
```

This completes the workshop — you've built a full AI-powered marketplace operations platform from data loading through to a deployed application, all in under 90 minutes!
""")


render_key_concepts([
    {"term": "Container Runtime", "definition": "The current SiS execution environment. Apps run on a compute pool, support any Python package via pip, and use versioned stage syntax. Replaces the legacy warehouse runtime."},
    {"term": "Compute Pool", "definition": "A managed pool of container nodes. Choose an instance family (CPU_X64_S, GPU_NV_S, etc.), set min/max nodes, and Snowflake handles provisioning and scaling."},
    {"term": "External Access Integration", "definition": "Required for container runtime apps that install pip packages. Container nodes can't reach the internet by default — you must allow egress to pypi.org via network rules."},
    {"term": "Streamlit in Snowflake (SiS)", "definition": "Snowflake's native app framework for Python data apps. Apps run on Snowflake compute, access data via Snowpark, and inherit security model. Deployed as first-class Snowflake objects."},
])

render_what_you_built([
    "HIIVE_COMPUTE_POOL — compute pool for container runtime",
    "MARKETPLACE_DASHBOARD — 2-page Streamlit app",
    "Marketplace Dashboard with KPIs, charts, and compliance table",
    "AI-powered chat interface connected to MARKETPLACE_OPS_AGENT",
])
