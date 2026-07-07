import streamlit as st

st.title("Getting Started")
st.markdown("Confirm your Snowflake access for the workshop")

st.space("small")

st.markdown("#### Step 1: Confirm account access")

with st.container(border=True):
    st.markdown("""
You already have a Snowflake account. Confirm you can log in and have the appropriate role:

1. Log in to your Snowflake account via Snowsight
2. Check your current role — you'll need **ACCOUNTADMIN** or a role with privileges to create databases, warehouses, and Cortex objects
3. If using a dedicated workshop role, ensure it has been granted the necessary privileges

:material/info: If you're unsure about role permissions, run:
```sql
SELECT CURRENT_ROLE(), CURRENT_ACCOUNT();
SHOW GRANTS TO ROLE <your_role>;
```
""")

st.space("small")

st.markdown("#### Step 2: Open Cortex Code")

with st.container(border=True):
    st.markdown("""
Once logged in to Snowsight, open **Cortex Code** from the left navigation panel. This is the AI coding assistant where you will paste all prompts from this workshop.

Confirm you are using the correct role — you can check and switch roles in the bottom-left of the Snowsight UI.
""")

st.space("small")

st.markdown("#### Step 3: Enable cross-region inference")

with st.container(border=True):
    st.markdown("""
Several sessions use Cortex LLM models that require cross-region inference. Enable it by running this SQL in a worksheet:

```sql
ALTER ACCOUNT SET CORTEX_ENABLED_CROSS_REGION = 'ANY_REGION';
```

This allows Snowflake to route LLM requests to the nearest available region if the model is not hosted in your account's home region.
""")

st.space("small")

st.markdown("#### Step 4 (Optional): Install Cortex Code Plugin in VS Code")

with st.container(border=True):
    st.markdown("""
If you'd like to use Cortex Code from VS Code alongside your existing Claude Code setup:

1. Open VS Code → Extensions → search **"Snowflake"** → Install
2. Command Palette (`Cmd+Shift+P`) → **"Snowflake: Sign In"**
3. Configure your connection in `~/.snowflake/connections.toml`

See the **Cortex Code Plugin** reference page in the sidebar for full setup details.

:material/warning: **Cloudflare VPN note**: If you encounter SSL certificate issues, you may need to set `insecure_mode = true` in your connection config or add Cloudflare's root cert to the trust store.
""")

st.space("small")

st.markdown("#### Quick verification")

col1, col2 = st.columns(2)
col1.metric("Required", "ACCOUNTADMIN", help="Or equivalent role with CREATE privileges")
col2.metric("Cross-region", "ANY_REGION", help="Enables Cortex LLM access across regions")

st.caption("Once you've confirmed access and enabled cross-region inference, you're ready to start Session 1")
