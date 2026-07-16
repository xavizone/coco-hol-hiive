import streamlit as st
import json

st.set_page_config(page_title="Marketplace Intelligence", page_icon="🤖", layout="wide")
st.title("🤖 Marketplace Intelligence Chat")

conn = st.connection("snowflake")
session = conn.session()

# --- Sidebar Stats ---
with st.sidebar:
    st.header("Summary Stats")
    trades = session.sql("SELECT COUNT(*) FROM TRADE_EXECUTIONS").collect()[0][0]
    listings = session.sql("SELECT COUNT(*) FROM LISTINGS WHERE STATUS = 'active'").collect()[0][0]
    companies = session.sql("SELECT COUNT(*) FROM COMPANIES").collect()[0][0]
    st.metric("Total Trades", trades)
    st.metric("Active Listings", listings)
    st.metric("Companies Tracked", companies)

# --- Chat Interface ---
if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Ask about marketplace operations..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            try:
                request_body = json.dumps({
                    "messages": [{"role": "user", "content": [{"type": "text", "text": prompt}]}],
                    "stream": False
                })
                result = session.sql(f"""
                    SELECT SNOWFLAKE.CORTEX.DATA_AGENT_RUN(
                        'HIIVE_COCO_HOL.{session.sql("SELECT CURRENT_SCHEMA()").collect()[0][0]}.MARKETPLACE_OPS_AGENT',
                        '{request_body.replace("'", "''")}'
                    )
                """).collect()

                response_json = json.loads(result[0][0])
                # Extract text content from response
                answer_parts = []
                if "content" in response_json:
                    for block in response_json["content"]:
                        if block.get("type") == "text" and block.get("text", "").strip():
                            answer_parts.append(block["text"])

                answer = "\n".join(answer_parts) if answer_parts else "I received a response but couldn't extract text content."
                st.markdown(answer)
                st.session_state.messages.append({"role": "assistant", "content": answer})
            except Exception as e:
                error_msg = f"Error querying agent: {str(e)}"
                st.error(error_msg)
                st.session_state.messages.append({"role": "assistant", "content": error_msg})
