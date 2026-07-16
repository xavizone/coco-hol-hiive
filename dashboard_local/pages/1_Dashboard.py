import streamlit as st
import json

st.set_page_config(page_title="Marketplace Dashboard", page_icon="📊", layout="wide")
st.title("📊 Marketplace Dashboard")

conn = st.connection("snowflake")
session = conn.session()

# --- KPI Cards ---
col1, col2, col3, col4 = st.columns(4)

with col1:
    result = session.sql("SELECT SUM(TOTAL_VALUE_USD) FROM TRADE_EXECUTIONS").collect()
    total_volume = result[0][0] if result[0][0] else 0
    st.metric("Total Trade Volume", f"${total_volume:,.0f}")

with col2:
    result = session.sql("SELECT COUNT(*) FROM LISTINGS WHERE STATUS = 'active'").collect()
    active_listings = result[0][0]
    st.metric("Active Listings", f"{active_listings}")

with col3:
    result = session.sql("SELECT AVG(EXECUTION_PRICE_PER_SHARE) FROM TRADE_EXECUTIONS").collect()
    avg_price = result[0][0] if result[0][0] else 0
    st.metric("Avg Execution Price", f"${avg_price:,.2f}")

with col4:
    result = session.sql("SELECT ROUND(COUNT(CASE WHEN OUTCOME = 'approved' THEN 1 END) * 100.0 / COUNT(*), 1) FROM COMPLIANCE_REVIEWS").collect()
    approval_rate = result[0][0] if result[0][0] else 0
    st.metric("Compliance Approval Rate", f"{approval_rate}%")

st.markdown("---")

# --- Trade Volume by Company ---
st.subheader("Trade Volume by Company")
volume_df = session.sql("""
    SELECT c.COMPANY_NAME, SUM(t.TOTAL_VALUE_USD) as TRADE_VOLUME
    FROM TRADE_EXECUTIONS t
    JOIN COMPANIES c ON t.COMPANY_ID = c.COMPANY_ID
    GROUP BY c.COMPANY_NAME
    ORDER BY TRADE_VOLUME DESC
    LIMIT 10
""").to_pandas()

st.bar_chart(volume_df.set_index("COMPANY_NAME")["TRADE_VOLUME"])

# --- Daily Trades Over Time ---
st.subheader("Daily Trades Over Time")
trades_df = session.sql("""
    SELECT TRADE_DATE, COUNT(*) as TRADE_COUNT, SUM(TOTAL_VALUE_USD) as DAILY_VOLUME
    FROM TRADE_EXECUTIONS
    GROUP BY TRADE_DATE
    ORDER BY TRADE_DATE
""").to_pandas()

if not trades_df.empty:
    st.line_chart(trades_df.set_index("TRADE_DATE")["DAILY_VOLUME"])
else:
    st.info("No trade date data available for time series chart.")

# --- Compliance Reviews Table ---
st.subheader("Recent Compliance Reviews")
compliance_df = session.sql("""
    SELECT REVIEW_ID, REVIEW_TYPE, OUTCOME, RISK_SCORE, REVIEW_DATE
    FROM COMPLIANCE_REVIEWS
    ORDER BY RISK_SCORE DESC
    LIMIT 20
""").to_pandas()

def color_risk(val):
    if val >= 0.7:
        return "background-color: #ffcccc"
    elif val >= 0.4:
        return "background-color: #fff3cd"
    else:
        return "background-color: #d4edda"

if not compliance_df.empty:
    styled = compliance_df.style.map(color_risk, subset=["RISK_SCORE"])
    st.dataframe(styled, use_container_width=True)
else:
    st.info("No compliance review data available.")
