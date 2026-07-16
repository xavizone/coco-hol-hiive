import streamlit as st

st.title("Workshop agenda")

st.markdown("""
**Target duration: ~90 minutes** — Some labs can be skipped during the live session and completed independently afterward.
""")

st.markdown("---")

# Block 1
st.markdown("#### Block 1: Data & Intelligence :gray-badge[~35 min]")
st.markdown("""
| Session | Title | Description |
|---------|-------|-------------|
| 1 | Data Prep | Personal schema + 10 marketplace tables loaded from shared stage |
| 2 | Cortex Analyst & Semantic Views | Semantic view with relationships, metrics, and NL queries |
| 3 | Cortex Search | Knowledge base, search service, and RAG query pattern |
""")

st.markdown("---")

# Block 2
st.markdown("#### Block 2: Agents & Apps :gray-badge[~20 min]")
st.markdown("""
| Session | Title | Description |
|---------|-------|-------------|
| 4 | Cortex Agents | Agent with Analyst + Search + custom UDF tools |
| 5 | CoWork | Collaborative AI analysis in Snowsight |
| 6 | Streamlit | Operations dashboard with AI chat interface |
""")

st.markdown("---")

# Block 3
st.markdown("#### Block 3: Monitoring & Quality :gray-badge[~15 min]")
st.markdown("""
| Session | Title | Description |
|---------|-------|-------------|
| 7 | DMF & Monitoring | System + custom DMFs, scheduling, alerts, anomaly detection |
""")

st.markdown("---")

# Block 4
st.markdown("#### Block 4: Data Pipelines :gray-badge[~20 min]")
st.markdown("""
| Session | Title | Description |
|---------|-------|-------------|
| 8 | dbt Projects | Deploy, execute, and schedule a dbt project natively in Snowflake |
| 9 | dbt Projects (Hands-On) | Version, rollback, task chains — full CLI + SQL workflow |
""")
st.caption("Sessions 8-9 can be combined or done independently after the workshop.")

st.space("medium")

st.markdown("##### What you'll build by end of session")
st.markdown("""
| Object Type | Count | Examples |
|-------------|-------|---------|
| **Tables** | 10 | Trade executions, listings, pricing signals, compliance reviews |
| **Cortex Search Services** | 1 | Compliance & regulatory document search |
| **Semantic Views** | 1 | MARKETPLACE_ANALYTICS_VIEW with relationships, metrics, and AI instructions |
| **Cortex Agents** | 1 | Marketplace operations agent with Analyst + Search + custom tools |
| **Streamlit Apps** | 1 | Operations dashboard with AI chat |
| **Data Metric Functions** | 8 | 5 system DMFs (NULL_COUNT, ROW_COUNT, FRESHNESS) + 3 custom anomaly detection |
| **Alerts** | 1 | Trade volume anomaly alert |
| **dbt Projects** | 1 | Native Snowflake dbt project with staging views + mart table |
| **Snowflake Tasks** | 2 | Task chain: DBT_SCHEDULED_RUN → DBT_SCHEDULED_TEST |
""")

st.space("small")

st.markdown("##### Location")
with st.container(border=True):
    st.markdown("""
:material/location_on: **HIIVE Office**

July 16, 2026 — Starting at 10:00 AM (~90 min)
""")
