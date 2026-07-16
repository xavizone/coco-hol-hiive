import streamlit as st
from components import render_session_header, render_prompt, render_explanation, render_technologies_used, render_key_concepts, render_what_you_built, render_docs_links, render_execution_context

render_session_header(4, "Cortex Agents", "10:50 - 11:00 AM", "10 min", "Cortex Agent with Analyst + Search + custom tools")

render_technologies_used([
    {"name": "Cortex Agent (CREATE AGENT)", "description": "An orchestrating AI that plans tasks, selects tools (Analyst, Search, custom), executes them, reflects on results, and generates responses. Created as a first-class Snowflake object.", "icon": "smart_toy"},
    {"name": "Tool Orchestration", "description": "The Agent automatically routes questions to the right tool: Cortex Analyst for structured data, Cortex Search for unstructured documents, custom UDFs for business logic.", "icon": "route"},
    {"name": "Custom Tools (UDFs)", "description": "User-defined functions that extend Agent capabilities. The Agent can call any SQL UDF as a tool, enabling custom business logic and calculations.", "icon": "build"},
])

st.markdown("""
> **Context check:** Verify your session is using `HIIVE_COCO_HOL_ROLE`, `HIIVE_COCO_HOL_WH`, and `HIIVE_COCO_HOL` database with your personal schema. If anything looks off, run:
> ```sql
> USE ROLE HIIVE_COCO_HOL_ROLE;
> USE WAREHOUSE HIIVE_COCO_HOL_WH;
> USE DATABASE HIIVE_COCO_HOL;
> USE SCHEMA <YOUR_USERNAME>_OPS;
> ```
""")

render_execution_context("cortex_code")


PROMPT_4_1 = """You are a Cortex Agent expert with full knowledge of the latest CREATE AGENT DDL syntax. In my workshop schema in HIIVE_COCO_HOL, create a Cortex Agent called MARKETPLACE_OPS_AGENT that marketplace operations staff can use to ask questions about both structured data and unstructured documents.

The agent spec uses a YAML format within FROM SPECIFICATION $$...$$. Key structural rules:
- models: section with orchestration: auto
- tools: list of tool_spec entries (type, name, description)
- tool_resources: TOP-LEVEL key (not nested under each tool), keyed by tool name
  - For cortex_analyst_text_to_sql: needs semantic_view and execution_environment (type: warehouse, warehouse: HIIVE_COCO_HOL_WH)
  - For cortex_search: needs search_service (not cortex_search_service)
- instructions: has sub-keys orchestration: and response:
- sample_questions: nested under instructions, uses format: - question: "..."

The agent should:
- Use auto as the orchestration model
- Have two tools:
  - marketplace_analytics (cortex_analyst_text_to_sql) using the MARKETPLACE_ANALYTICS_VIEW semantic view
  - marketplace_knowledge (cortex_search) using the MARKETPLACE_KNOWLEDGE_SEARCH service
- Instructions should define it as the HIIVE Marketplace Operations Assistant with:
  - Tool routing: structured data questions to analytics, compliance/regulatory/support to search
  - Domain context: HIIVE is a pre-IPO secondary trading platform. ROFR, 409A, accredited investors
- Include 3-4 sample questions spanning both tools

Execute and confirm with DESCRIBE AGENT or SHOW AGENTS."""

render_prompt("Prompt 4.1", "Create the Cortex Agent", PROMPT_4_1)

render_explanation("What this prompt does", """
Creates a **Cortex Agent** — an AI orchestrator that combines multiple data tools.

**CREATE AGENT YAML structure** (this is the exact structure that works):

```yaml
CREATE OR REPLACE AGENT my_agent
FROM SPECIFICATION $$
models:
  orchestration: auto
tools:
  - tool_spec:
      type: cortex_analyst_text_to_sql
      name: my_analyst_tool
      description: "..."
  - tool_spec:
      type: cortex_search
      name: my_search_tool
      description: "..."
tool_resources:                          # <-- TOP-LEVEL, not nested per tool
  my_analyst_tool:
    semantic_view: DB.SCHEMA.MY_VIEW
    execution_environment:
      type: warehouse
      warehouse: MY_WH
  my_search_tool:
    search_service: DB.SCHEMA.MY_SEARCH  # <-- "search_service" not "cortex_search_service"
instructions:
  orchestration: |
    Your orchestration instructions here...
  response: |
    Your response formatting instructions here...
  sample_questions:
    - question: "Example question 1"
    - question: "Example question 2"
$$;
```

**Critical syntax gotchas**:
- `tool_resources` is a **top-level** YAML key, not nested under each tool
- Cortex Search uses `search_service` (not `cortex_search_service`)
- Analyst tools **require** `execution_environment` with a warehouse
- `instructions` has sub-keys: `orchestration`, `response`, `sample_questions`
""")


PROMPT_4_2 = """Test our MARKETPLACE_OPS_AGENT by running queries through SNOWFLAKE.CORTEX.DATA_AGENT_RUN(). Run these queries:

1. Structured data query: "What are the top companies by total trade volume and which sectors dominate?"
2. Unstructured search query: "Have there been any KYC failures or compliance escalations recently? What happened?"
3. Trend query: "What is the trend in daily active users over the last quarter?"

Use this invocation pattern:
SELECT SNOWFLAKE.CORTEX.DATA_AGENT_RUN(
  'HIIVE_COCO_HOL.<YOUR_USERNAME>_OPS.MARKETPLACE_OPS_AGENT',
  '{"messages": [{"role": "user", "content": [{"type": "text", "text": "<question>"}]}], "stream": false}'
) as response;

For each, show the response and note which tools the agent chose to use."""

render_prompt("Prompt 4.2", "Test the Agent", PROMPT_4_2)

render_explanation("What this prompt does", """
Tests the Agent with three question types that exercise different tool routing:

1. **Pure structured** — routes to Cortex Analyst, generates SQL with GROUP BY company/sector for trade volumes
2. **Pure unstructured** — routes to Cortex Search, retrieves KYC failure and compliance escalation documents
3. **Trend analysis** — routes to Analyst for time-series query on platform activity metrics

**Invoking the agent via SQL**:
```sql
SELECT SNOWFLAKE.CORTEX.DATA_AGENT_RUN(
  'DB.SCHEMA.AGENT_NAME',
  '{"messages": [{"role": "user", "content": [{"type": "text", "text": "your question"}]}], "stream": false}'
) as response;
```

**What to look for in the response JSON**:
- `tool_use` entries show which tools the agent selected
- `tool_result` entries contain the actual data returned
- The final `text` entry is the agent's synthesized response

> **Tip**: You can also test agents in the Snowsight UI. Go to **AI & ML → Snowflake Intelligence** and select your agent to chat with it interactively.
""")


PROMPT_4_3 = """In my workshop schema in HIIVE_COCO_HOL, enhance our agent by adding a custom tool.

1. Create a UDF that calculates trade risk score:

CREATE OR REPLACE FUNCTION CALCULATE_TRADE_RISK_SCORE(
    company_name VARCHAR,
    trade_value NUMBER,
    shares_pct_of_outstanding NUMBER
)
RETURNS OBJECT
LANGUAGE SQL
AS
$$
    SELECT OBJECT_CONSTRUCT(
        'company', company_name,
        'trade_value', trade_value,
        'shares_pct_of_outstanding', shares_pct_of_outstanding,
        'risk_score',
            CASE
                WHEN trade_value > 1000000 AND shares_pct_of_outstanding > 5 THEN 'HIGH'
                WHEN trade_value > 500000 OR shares_pct_of_outstanding > 2 THEN 'MEDIUM'
                ELSE 'LOW'
            END,
        'recommendation',
            CASE
                WHEN trade_value > 1000000 AND shares_pct_of_outstanding > 5 THEN 'Large block trade - may trigger ROFR. Require issuer notification and 30-day waiting period. Verify accredited investor status.'
                WHEN trade_value > 500000 OR shares_pct_of_outstanding > 2 THEN 'Elevated trade - enhanced KYC review recommended. Monitor for wash trading patterns.'
                ELSE 'Standard trade - proceed with normal settlement workflow.'
            END
    )
$$;

2. Test the UDF with sample inputs.

3. Recreate MARKETPLACE_OPS_AGENT to include CALCULATE_TRADE_RISK_SCORE as an additional custom tool alongside the existing Analyst and Search tools. For custom tools in the agent spec:
   - tool_spec type is "function"
   - tool_resources for the function needs: function_name, description of parameters

4. Test the enhanced agent with: "What is the risk score for a $2M trade of 8% of Stripe's outstanding shares?"

Execute all SQL and show results."""

render_prompt("Prompt 4.3", "Agent with Custom Tool", PROMPT_4_3)

render_explanation("What this prompt does", """
Extends the Agent with a **custom UDF tool**:

**Custom tools** allow Agents to go beyond Search and Analyst:
- Business calculations (trade risk scoring)
- Compliance checks (ROFR triggers, accreditation verification)
- Data transformations (price normalization, volume calculations)
- Workflow triggers (flagging trades for review, sending notifications)

**The UDF** implements a rule-based trade risk calculator:
- **HIGH**: Trade > $1M AND shares > 5% of outstanding — large block that may trigger Right of First Refusal
- **MEDIUM**: Trade > $500K OR shares > 2% — enhanced KYC review needed
- **LOW**: Standard trade — normal settlement workflow

**How the Agent uses custom tools**: When the user asks about trade risk, the Agent:
1. Recognizes this matches the CALCULATE_TRADE_RISK_SCORE function
2. Extracts parameters (company=Stripe, trade_value=2000000, shares_pct=8)
3. Calls the UDF with those parameters
4. Incorporates the result into its response

**This is the "agentic" pattern**: The Agent doesn't just retrieve data — it takes actions, calls functions, and orchestrates workflows.

> **Note**: Adding custom tools (type: "function") to agents requires the function to be accessible to the agent's execution role. The agent spec references the function by its fully qualified name.
""")


render_key_concepts([
    {"term": "Cortex Agent", "definition": "A first-class Snowflake object that orchestrates LLMs, Cortex Analyst, Cortex Search, and custom tools to answer complex questions. Created with CREATE AGENT FROM SPECIFICATION using YAML config."},
    {"term": "Tool Routing", "definition": "The Agent's ability to select the appropriate tool for each question. Structured data -> Analyst, unstructured search -> Search, calculations -> custom UDFs. The orchestration LLM decides routing."},
    {"term": "tool_resources", "definition": "A TOP-LEVEL YAML key in the agent spec (not nested per tool). Maps tool names to their resources: semantic_view + execution_environment for Analyst, search_service for Search."},
    {"term": "DATA_AGENT_RUN", "definition": "The SQL function to invoke a Cortex Agent. Takes the agent's fully qualified name and a JSON request body with messages array. Returns a JSON response with tool calls and synthesized answer."},
])

render_docs_links([
    {"title": "Cortex Agents", "url": "https://docs.snowflake.com/en/user-guide/snowflake-cortex/cortex-agent"},
    {"title": "CREATE AGENT", "url": "https://docs.snowflake.com/en/sql-reference/sql/create-agent"},
    {"title": "User-Defined Functions (UDFs)", "url": "https://docs.snowflake.com/en/developer-guide/udf/udf-overview"},
    {"title": "DATA_AGENT_RUN", "url": "https://docs.snowflake.com/en/sql-reference/functions/data_agent_run"},
])

render_what_you_built([
    "MARKETPLACE_OPS_AGENT — Cortex Agent with Analyst + Search tools",
    "Tested structured, unstructured, and trend queries via DATA_AGENT_RUN",
    "CALCULATE_TRADE_RISK_SCORE UDF as a custom tool",
    "Enhanced agent with three tool types (Analyst + Search + custom)",
])
