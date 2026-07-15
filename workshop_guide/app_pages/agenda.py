import streamlit as st

st.title("Workshop agenda")

AGENDA = [
    ("10:00 - 10:05 AM", "Welcome & Overview", None, None),
    ("10:05 - 10:20 AM", "Session 1: Data Prep", "15 min", "1"),
    ("10:20 - 10:35 AM", "Session 2: Cortex Analyst & Semantic Views", "15 min", "2"),
    ("10:35 - 10:45 AM", "Session 3: Cortex Search", "10 min", "3"),
    ("10:45 - 10:50 AM", ":orange-badge[BREAK]", None, None),
    ("10:50 - 11:00 AM", "Session 4: Cortex Agents", "10 min", "4"),
    ("11:00 - 11:05 AM", "Session 5: CoWork", "5 min", "5"),
    ("11:05 - 11:10 AM", "Session 6: Streamlit", "5 min", "6"),
    ("11:10 - 11:25 AM", "Session 7: DMF & Monitoring", "15 min", "7"),
    ("11:25 - 11:45 AM", "Session 8: dbt Projects", "20 min", "8"),
    ("11:45 - 11:50 AM", ":gray[Wrap-up & Q&A]", None, None),
]

for time, title, duration, session_num in AGENDA:
    if session_num:
        col1, col2 = st.columns([1, 4])
        col1.markdown(f"**{time}**")
        col2.markdown(f":material/play_circle: **{title}** :gray-badge[{duration}]")
    elif "BREAK" in title:
        col1, col2 = st.columns([1, 4])
        col1.markdown(f"**{time}**")
        col2.markdown(f"{title}")
    else:
        col1, col2 = st.columns([1, 4])
        col1.markdown(f"**{time}**")
        col2.markdown(f":gray[{title}]")

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
| **Data Metric Functions** | 6 | System DMFs + custom anomaly detection |
| **Alerts** | 1 | Trade volume anomaly alert |
| **dbt Projects** | 1 | Native Snowflake dbt project with staging + mart models |
""")

st.space("small")

st.markdown("##### Location")
with st.container(border=True):
    st.markdown("""
:material/location_on: **HIIVE Office**

July 16, 2026 — 10:00 AM to 11:30 AM
""")
