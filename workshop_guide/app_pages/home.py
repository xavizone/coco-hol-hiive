import streamlit as st
from pathlib import Path

_STATIC = Path(__file__).parent.parent / "static"

logo_col1, logo_col2 = st.columns(2)
with logo_col1:
    st.image(str(_STATIC / "Hiive_Logo.png"), width=150)
with logo_col2:
    st.image(str(_STATIC / "snowflake_full_logo.png"), width=180)

st.title("HIIVE Snowflake CoCo Workshop")
st.markdown("From Reactive Monitoring to Proactive Data Intelligence with Snowflake")

st.space("small")

col1, col2, col3 = st.columns(3)
col1.metric("Sections", "9", help="Hands-on lab sections across 4 blocks")
col2.metric("Prompts", "20+", help="Guided prompts plus hands-on CLI steps")
col3.metric("Duration", "~90 min", help="Core workshop time (additional labs can be completed after)")

st.space("medium")

st.markdown("#### How this workshop works")

st.markdown("""
Each section has **numbered prompts** that you copy and paste into the appropriate tool:

- **Cortex Code** — for building infrastructure, creating objects, and writing SQL/Python
- **Cortex Analyst** — for testing natural language queries against your semantic view
- **Snowflake CoWork** — for collaborative data exploration and analysis

All prompts build on each other sequentially — run them in order throughout the session.
""")

st.space("small")

st.markdown("#### The scenario")
with st.container(border=True):
    st.markdown("""
**HIIVE** is a private securities marketplace connecting sellers of pre-IPO shares with accredited buyers.
As a platform facilitating secondary trading, data quality and monitoring are critical — every trade
involves compliance reviews, pricing validation, and regulatory oversight.

We'll build a complete AI platform covering:

| Data type | Examples |
|-----------|---------|
| **Structured** | Trade executions, listings, pricing signals, platform metrics |
| **Unstructured** | Compliance reviews, support tickets, regulatory filings |
| **Time series** | Platform activity, user sessions, trade volume trends |
""")

st.space("small")

st.markdown("#### What we're building")

with st.container(border=True):
    st.markdown("""
In ~90 minutes, we build a complete AI-powered marketplace intelligence platform:

**1. Data Foundation** — Load marketplace and compliance data into Snowflake from pre-generated CSV files.

**2. Natural Language Analytics** — Create a Semantic View over trade/pricing/listing tables and query them with plain English via Cortex Analyst.

**3. Intelligent Search** — Build a Cortex Search service over compliance reviews and regulatory documents for hybrid semantic + keyword search.

**4. AI Agents** — Create a Cortex Agent that orchestrates structured data queries AND document search through a single conversational interface.

**5. Collaborative AI** — Use CoWork to collaboratively analyze marketplace data with AI assistance.

**6. Operations Dashboard** — Deploy a Streamlit app with live KPIs, charts, and an AI chat interface.

**7. Proactive Monitoring** — Build Data Metric Functions for anomaly detection and automated alerting — filling the gap between dbt runs.

**8. Native dbt Pipelines** — Deploy a dbt project as a first-class Snowflake object and replace GitHub Actions with a Snowflake Task.

**9. dbt Hands-On** — Execute, version, rollback, and schedule dbt projects using SQL and CLI — the full developer workflow.
""")

st.space("small")

st.markdown("#### Prerequisites")
with st.container(border=True):
    st.markdown("""
- Your own dev/Sandbox Snowflake account or a Trial Snowflake account with **ACCOUNTADMIN** role [**Snowflake Trial** Account](signup.snowflake.com);
- **Cortex Code** open in Snowsight and connected to your account
- **Snowflake CLI** installed (`brew install snowflake-cli`) — required for Sessions 8-9 (dbt deployment)
- Cross-region inference enabled (for Cortex LLM functions)
- Admin has pre-configured `HIIVE_COCO_HOL` database, warehouse (`HIIVE_COCO_HOL_WH`), and shared resources
- Your personal schema will be created automatically using your Snowflake username (e.g., `HIIVE_COCO_HOL.XAVIER_OPS`)
- See the **Getting Started** page for detailed environment setup instructions
""")

st.space("medium")
st.caption("Built for the July 16, 2026 workshop at HIIVE")
