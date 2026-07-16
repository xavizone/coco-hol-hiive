import streamlit as st

st.title("Getting Started")
st.markdown("Attendee prerequisites and day-of verification")

# ─────────────────────────────────────────────────────────────────────────────
# Attendee Prerequisites
# ─────────────────────────────────────────────────────────────────────────────

st.markdown("#### :material/laptop: What to bring / install before the session")
with st.container(border=True):
    st.markdown("""
| Item | Details |
|------|---------|
| **Laptop with Chrome** | We'll be working in Snowsight (browser-based) for Blocks 1-3 |
| **Snowflake account access** | You'll receive `HIIVE_COCO_HOL_ROLE` credentials from your admin before the session |
| **Snowflake CLI** | `brew install snowflake-cli` (Mac) or [docs.snowflake.com/developer-guide/snowflake-cli](https://docs.snowflake.com/en/developer-guide/snowflake-cli/index) — required for Sessions 8-9 (dbt) |
| **VS Code** | With the **Snowflake extension** installed (search "Snowflake" in Extensions marketplace) |

:material/info: **Blocks 1-3 use Cortex Code in Snowsight** (browser). The VS Code + CoCo plugin is covered in the Reference section and is optional for the hands-on portion but recommended for daily workflow after.
""")

st.markdown("---")

# ─────────────────────────────────────────────────────────────────────────────
# Day-of Verification
# ─────────────────────────────────────────────────────────────────────────────

st.markdown("#### :material/checklist: Verify your setup (day-of, before 10:00 AM)")

st.markdown("##### 1. Verify login")
with st.container(border=True):
    st.markdown("Log into **Snowsight** with your HIIVE credentials and confirm you have access.")

st.markdown("##### 2. Check role")
with st.container(border=True):
    st.markdown("Confirm you have `HIIVE_COCO_HOL_ROLE` assigned:")
    st.code("""USE ROLE HIIVE_COCO_HOL_ROLE;
USE WAREHOUSE HIIVE_COCO_HOL_WH;
SELECT CURRENT_ROLE(), CURRENT_USER();""", language="sql")

st.markdown("##### 3. Verify shared resources are visible")
with st.container(border=True):
    st.markdown("Run the following to confirm the shared stage is accessible:")
    st.code("LIST @HIIVE_COCO_HOL.SHARED_DATA.WORKSHOP_FILES;", language="sql")
    st.markdown("You should see **10 CSV files** listed.")

st.markdown("##### 4. Understand the naming convention")
with st.container(border=True):
    st.markdown("""
Your personal schema will be created automatically using your Snowflake username (e.g., if you're logged in as OLEG, your schema will be `HIIVE_COCO_HOL.OLEG_OPS`).

This prevents object collisions between attendees — everyone works in their own namespace.
""")

st.markdown("##### 5. Open Cortex Code")
with st.container(border=True):
    st.markdown("""
In Snowsight, open **Cortex Code** from the left navigation panel. This is where you'll paste all prompts from this workshop.

You can check and switch roles in the bottom-left of the Snowsight UI.
""")

st.markdown("##### 6. (Optional) VS Code + CoCo Plugin")
with st.container(border=True):
    st.markdown("""
If you'd like to use Cortex Code from VS Code:

1. Open VS Code → Extensions → search **"Snowflake"** → Install
2. Command Palette (`Cmd+Shift+P`) → **"Snowflake: Sign In"**
3. Configure your connection in `~/.snowflake/connections.toml`

See the **Reference** page in the sidebar for full setup details.

:material/warning: **Cloudflare VPN note**: If you're behind Cloudflare VPN and see SSL certificate errors, add `insecure_mode = true` under your connection block in `~/.snowflake/connections.toml`:

```toml
[default]
insecure_mode = true
```

This disables certificate verification for that connection. Remove it once you're off the VPN or the cert issue is resolved.
""")

# ─────────────────────────────────────────────────────────────────────────────
# Troubleshooting
# ─────────────────────────────────────────────────────────────────────────────

st.markdown("---")

st.markdown("#### :material/build: If Something Doesn't Work")

with st.container(border=True):
    st.markdown("""
| Problem | Fix |
|---------|-----|
| **Can't see the role** | Ask your admin to run `GRANT ROLE HIIVE_COCO_HOL_ROLE TO USER <your_username>;` |
| **SSL/VPN certificate errors** | Open `~/.snowflake/connections.toml` and add `insecure_mode = true` under your connection block |
| **Cortex Code not appearing in Snowsight** | Ensure you're on the correct role (`HIIVE_COCO_HOL_ROLE`) — check bottom-left of Snowsight UI |
| **CLI install issues** | The lab works entirely in-browser via Snowsight. CLI is only needed for Sessions 8-9 (dbt). |
| **"Object does not exist" errors** | Make sure you ran Session 1 prompts first — they create your personal schema and tables |
""")

# ─────────────────────────────────────────────────────────────────────────────
# Quick Reference
# ─────────────────────────────────────────────────────────────────────────────

st.space("small")
st.divider()

st.markdown("#### Quick reference")

col1, col2, col3 = st.columns(3)
col1.metric("Role", "HIIVE_COCO_HOL_ROLE", help="Pre-assigned by admin")
col2.metric("Warehouse", "HIIVE_COCO_HOL_WH", help="Shared Medium warehouse")
col3.metric("Duration", "~90 min", help="Core workshop time")

st.caption("All prompts build sequentially — run them in order. Once you've confirmed access, you're ready to start Session 1.")
