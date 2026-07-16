import streamlit as st

st.title("Reference: Snowflake AI Assistants")
st.markdown("A guide to Cortex Code, CoWork, and how they fit into your workflow")

st.space("small")

# ─────────────────────────────────────────────────────────────────────────────
# Overview: All Options at a Glance
# ─────────────────────────────────────────────────────────────────────────────

st.markdown("## :material/compare_arrows: All AI Assistant Options at a Glance")

with st.container(border=True):
    st.markdown("""
| Option | Where it runs | Best for | Persona |
|--------|--------------|----------|---------|
| **Cortex Code (Snowsight)** | Browser — built into Snowflake UI | Quick SQL, object creation, exploration | Analysts, Data Engineers, anyone in Snowsight |
| **Cortex Code (VS Code)** | VS Code extension | Multi-file projects, dbt, daily dev | Data Engineers, Platform Engineers |
| **Cortex Code (Desktop)** | Standalone desktop app | Full-featured coding + Snowflake | Power users, daily driver |
| **Cortex Code (CLI)** | Terminal | Automation, scripting, CI/CD | Advanced users, DevOps |
| **CoCo as MCP Plugin (Claude Code)** | Claude Code CLI | Combined code editing + Snowflake context | Teams already using Claude Code |
| **CoWork** | Browser — Snowsight collaborative space | Data exploration, insights, team sharing | Analysts, Business users, cross-functional teams |
""")

st.markdown("---")

# ─────────────────────────────────────────────────────────────────────────────
# Section 1: Cortex Code (Snowsight)
# ─────────────────────────────────────────────────────────────────────────────

st.markdown("## :material/web: Cortex Code in Snowsight")

with st.container(border=True):
    st.markdown("""
**What it is:** An AI coding assistant built directly into the Snowflake web UI (Snowsight). No installation needed — just open it from the left navigation panel.

**Best for:**
- Quick SQL exploration and ad-hoc queries
- Creating Snowflake objects (tables, views, semantic views, agents, DMFs)
- Iterating on semantic views with instant validation
- One-off data tasks where you don't need file editing

**How to access:** Snowsight → Left sidebar → Cortex Code

**Key capabilities:**
- Schema-aware query generation (knows your tables and columns)
- Execute SQL and see results inline
- Create and modify Snowflake objects with DDL
- Cortex Agent and Search service creation
- DMF management and monitoring queries

**Used in this workshop:** Sessions 1-7 (all prompt-based sessions)
""")

# ─────────────────────────────────────────────────────────────────────────────
# Section 2: Cortex Code (VS Code)
# ─────────────────────────────────────────────────────────────────────────────

st.markdown("## :material/extension: Cortex Code in VS Code")

with st.container(border=True):
    st.markdown("""
**What it is:** The Snowflake extension for VS Code includes Cortex Code as an integrated AI assistant with access to your local files AND Snowflake.

**Best for:**
- Multi-file projects (dbt models, Streamlit apps)
- Development workflows requiring terminal access (`snow dbt deploy`, CLI commands)
- Git-integrated Snowflake work (branch, edit, validate, commit)
- Daily development workflow where you live in VS Code

**Installation:**
1. VS Code → Extensions → search **"Snowflake"** → Install
2. Command Palette (`Cmd+Shift+P`) → **"Snowflake: Sign In"**
3. Configure connection in `~/.snowflake/connections.toml`

**Key capabilities (beyond Snowsight):**
- File editing and multi-file navigation
- Terminal access for CLI commands (`snow dbt deploy/execute`)
- Git integration (branch, diff, commit alongside SQL work)
- Workspace-level project context
- Local Streamlit app development and deployment

**Used in this workshop:** Sessions 8-9 (dbt deployment and CLI workflows)
""")

    st.code("""[hiive_coco_hol]
account = "your_account"
user = "your_user"
authenticator = "externalbrowser"
warehouse = "HIIVE_COCO_HOL_WH"
database = "HIIVE_COCO_HOL"
schema = ""  # Leave blank - set per session
""", language="toml")

    st.markdown("""
:material/warning: **VPN note**: If behind Cloudflare VPN and seeing SSL errors, add `insecure_mode = true` to your connection block.
""")

# ─────────────────────────────────────────────────────────────────────────────
# Section 3: Cortex Code Desktop
# ─────────────────────────────────────────────────────────────────────────────

st.markdown("## :material/desktop_windows: Cortex Code Desktop")

with st.container(border=True):
    st.markdown("""
**What it is:** A standalone desktop application that provides the full Cortex Code experience without requiring VS Code or a browser. It's a purpose-built coding environment with native Snowflake integration.

**Best for:**
- Teams who want a dedicated AI coding tool (not tied to an existing IDE)
- Full-featured development with Snowflake context built in
- Users who prefer a standalone app over browser-based or IDE-embedded tools
- Quick access without opening VS Code or Snowsight

**Key capabilities:**
- Full terminal access and file system navigation
- All Cortex Code tools (SQL execution, schema discovery, semantic views, dbt)
- Background agents and team workflows
- Scheduled automations and monitoring
- Plugin and MCP server support
- Multi-session management with resume capability

**Installation:**
- Download from [Snowflake's Cortex Code page](https://docs.snowflake.com/en/user-guide/cortex-code/cortex-code)
- Or via CLI: `brew install --cask snowflake-cortex-code` (Mac)

**When to choose Desktop over VS Code:**
- You want Cortex Code as your primary coding tool, not an add-on
- You don't need VS Code's broader extension ecosystem
- You want faster startup and a purpose-built Snowflake experience
""")

# ─────────────────────────────────────────────────────────────────────────────
# Section 4: Cortex Code CLI
# ─────────────────────────────────────────────────────────────────────────────

st.markdown("## :material/terminal: Cortex Code CLI")

with st.container(border=True):
    st.markdown("""
**What it is:** A terminal-based interface for Cortex Code. Same AI capabilities, accessed from your shell.

**Best for:**
- Power users who live in the terminal
- Automation and scripting (scheduled tasks, CI/CD integration)
- Remote development (SSH into servers, pair with `tmux`)
- Headless environments without a GUI

**Installation:**
```bash
brew install snowflake-cortex-code   # Mac
```

**Key features:**
- All Cortex Code tools available via chat interface
- `/loop` for scheduled recurring tasks (cron-style)
- Background agents (`/background-agent`) for parallel work
- Team mode (`/team`) for multi-agent orchestration
- Session management with resume and fork
- MCP server support for extending capabilities
- Keyboard shortcuts for efficient navigation

**Unique CLI features not in other surfaces:**
- `/bypass` mode for auto-approving all tool calls
- `/ssh` for remote server sessions
- `/swarm` for mission control multi-agent orchestration
- Programmatic tool calling (batch/loop/filter multiple tools in one turn)
""")

# ─────────────────────────────────────────────────────────────────────────────
# Section 5: CoCo as MCP Plugin in Claude Code
# ─────────────────────────────────────────────────────────────────────────────

st.markdown("## :material/power: CoCo as a Plugin in Claude Code")

with st.container(border=True):
    st.markdown("""
**What it is:** Cortex Code can run as an MCP (Model Context Protocol) server, giving Claude Code (or any MCP-compatible AI tool) live Snowflake context.

**Best for:**
- Teams already using Claude Code daily who want Snowflake superpowers added
- Combined workflows: code editing + git + Snowflake execution in one conversation
- End-to-end automation (edit dbt model → deploy → execute → verify results)

**Setup:**

1. Install the Snowflake CLI and configure a connection in `~/.snowflake/connections.toml`
2. Add the Snowflake MCP server to your Claude Code config (`.claude/mcp_servers.json`):

```json
{
  "snowflake": {
    "command": "snow",
    "args": ["cortex", "mcp-server", "--connection", "your_connection_name"]
  }
}
```

3. Restart Claude Code — it now has access to Snowflake tools (query execution, object discovery, etc.)

**What Claude Code gains:**
- Live Snowflake schema awareness (tables, columns, types)
- Query execution directly from conversations
- Semantic view discovery and validation
- DDL generation with full context of existing objects
- Combines Claude's file editing + git workflow with Snowflake's data platform

**Benefits of the combined workflow:**
- **Single context**: Claude Code sees your code AND your Snowflake schema simultaneously
- **End-to-end automation**: Edit a dbt model → deploy → execute → verify — one conversation
- **Debugging with full context**: Query fails → Claude reads the model file, checks schema, fixes it
- **Git-integrated Snowflake work**: Branch, modify semantic view, validate, commit — one flow

**When to use CoCo-in-Claude vs standalone CoCo:**

| Scenario | CoCo in Claude Code | Standalone CoCo |
|----------|:-------------------:|:---------------:|
| Multi-file code edits + SQL validation | :white_check_mark: | |
| Git operations alongside Snowflake work | :white_check_mark: | |
| dbt model editing + native deployment | :white_check_mark: | |
| Quick SQL exploration and object creation | | :white_check_mark: |
| Semantic view development with live preview | | :white_check_mark: |
| Team members without Claude Code access | | :white_check_mark: |
""")

st.markdown("---")

# ─────────────────────────────────────────────────────────────────────────────
# Section 6: CoWork — Collaborative AI Analysis
# ─────────────────────────────────────────────────────────────────────────────

st.markdown("## :material/group: CoWork — Collaborative AI Analysis")

with st.container(border=True):
    st.markdown("""
**What it is:** CoWork is Snowflake's AI-powered collaborative workspace inside Snowsight. It's fundamentally different from Cortex Code — designed for **data exploration and team collaboration**, not coding.

**Key difference from Cortex Code:**

| Aspect | Cortex Code | CoWork |
|--------|-------------|--------|
| **Purpose** | Build objects, write SQL, create infrastructure | Explore data, generate insights, share findings |
| **Persona** | Data Engineers, Platform Engineers, Developers | Analysts, Business Users, Cross-functional teams |
| **Output** | DDL, SQL, dbt projects, deployed objects | Charts, insights, analysis narratives, shared reports |
| **Interaction** | Technical prompts → precise code execution | Natural questions → visual answers with context |
| **Collaboration** | Single-user (though results are shared objects) | Multi-user (share sessions, build on each other's work) |
| **SQL knowledge needed** | Helpful (you're building SQL-based objects) | Not required (CoWork generates and runs SQL for you) |
""")

st.markdown("#### Who CoWork is for")
with st.container(border=True):
    st.markdown("""
| Persona | How they use CoWork | Time-to-value improvement |
|---------|--------------------|-----------------------------|
| **Business Analyst** | Ask questions about data in natural language, get charts instantly | Minutes instead of hours writing SQL + formatting dashboards |
| **Product Manager** | Explore user metrics, feature adoption, A/B test results | Self-serve instead of filing data requests |
| **Executive** | Get answers about revenue, growth, performance | No waiting for analyst availability |
| **Data Analyst** | Rapid EDA, hypothesis testing, ad-hoc analysis | Skip the boilerplate, jump to insights |
| **Cross-functional team** | Collaborative investigation (incident review, campaign analysis) | Single shared workspace vs scattered Slack threads |
""")

st.markdown("#### Typical CoWork tasks")
with st.container(border=True):
    st.markdown("""
- "What's our trade volume trend over the last 30 days? Show by company."
- "Which companies have the highest compliance risk scores?"
- "Compare listing fill rates across sectors — are there outliers?"
- "Show me today's platform activity broken down by session type"
- "What happened to our user engagement this week vs last week?"

**How it works:**
1. Open CoWork in Snowsight (left sidebar)
2. Ask a question in natural language
3. CoWork discovers your tables, writes SQL, runs it, and presents results as charts/tables
4. Share the session with teammates — they can build on your analysis
5. Pin important findings for the team to reference later
""")

st.markdown("#### Why CoWork matters for time-to-value")
with st.container(border=True):
    st.markdown("""
**Without CoWork (traditional workflow):**
1. Business user has a question → files a request
2. Analyst receives request → writes SQL → tests → formats results → sends back
3. Follow-up question → repeat the cycle
4. **Elapsed time: hours to days**

**With CoWork:**
1. Business user asks the question directly → gets answer with visualization immediately
2. Follow-up question → answered in the same session, building on prior context
3. Share with team → everyone can add their questions to the same thread
4. **Elapsed time: seconds to minutes**

**Key benefits:**
- **Zero SQL required** — natural language queries with automatic table discovery
- **Automatic visualization** — CoWork picks appropriate chart types based on the data
- **Persistent context** — follow-up questions build on previous answers (no re-explaining)
- **Team collaboration** — shared sessions where multiple people contribute questions
- **Semantic view awareness** — CoWork uses your semantic views for accurate metric definitions
- **Audit trail** — every question and answer is recorded for compliance and reference
""")

st.markdown("---")

# ─────────────────────────────────────────────────────────────────────────────
# Section 7: Choosing the Right Tool
# ─────────────────────────────────────────────────────────────────────────────

st.markdown("## :material/route: Decision Guide: Which Tool Should I Use?")

with st.container(border=True):
    st.markdown("""
```
START
  │
  ├─ "I need to explore data and share insights with my team"
  │     └─ CoWork (Snowsight)
  │
  ├─ "I need to create/modify Snowflake objects (tables, views, agents, DMFs)"
  │     ├─ Quick one-off task? → Cortex Code (Snowsight)
  │     └─ Part of a larger project? → Cortex Code (VS Code or Desktop)
  │
  ├─ "I need to deploy/manage a dbt project"
  │     ├─ Using Claude Code already? → CoCo MCP Plugin
  │     └─ Otherwise → Cortex Code (VS Code, Desktop, or CLI)
  │
  ├─ "I need to automate Snowflake tasks on a schedule"
  │     └─ Cortex Code (CLI) with /loop or automations
  │
  ├─ "I need a standalone daily-driver coding tool with Snowflake built in"
  │     └─ Cortex Code Desktop
  │
  └─ "I want Snowflake context inside my existing Claude Code workflow"
        └─ CoCo MCP Plugin
```
""")

st.markdown("---")

# ─────────────────────────────────────────────────────────────────────────────
# Section 8: Documentation Links
# ─────────────────────────────────────────────────────────────────────────────

st.markdown("## :material/menu_book: Documentation")

with st.container(border=True):
    st.markdown("""
**Cortex Code:**
- [Cortex Code Overview](https://docs.snowflake.com/en/user-guide/cortex-code/cortex-code) — Full documentation
- [Cortex Code in Snowsight](https://docs.snowflake.com/en/user-guide/ui-snowsight/cortex-code) — Browser-based assistant
- [Snowflake Extension for VS Code](https://docs.snowflake.com/en/user-guide/vscode-ext) — Installation and configuration

**CoWork:**
- [Snowflake CoWork](https://docs.snowflake.com/en/user-guide/ui-snowsight/cowork) — Collaborative AI analysis

**Infrastructure:**
- [Snowflake CLI](https://docs.snowflake.com/en/developer-guide/snowflake-cli/index) — CLI installation and setup
- [Snowflake MCP Server](https://docs.snowflake.com/en/developer-guide/snowflake-cli/cortex/mcp-server) — CoCo as plugin for Claude Code and other AI tools
- [connections.toml Reference](https://docs.snowflake.com/en/developer-guide/snowflake-cli/connecting/specify-credentials) — Connection configuration
""")
