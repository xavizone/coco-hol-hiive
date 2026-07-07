import streamlit as st
from components import render_session_header, render_prompt, render_explanation, render_technologies_used, render_key_concepts, render_what_you_built

render_session_header(4, "Cortex Agents", "10:35 - 11:00 AM", "25 min", "Cortex Agent with Analyst + Search + custom tools")

render_technologies_used([
    {"name": "Cortex Agent (CREATE AGENT)", "description": "An orchestrating AI that plans tasks, selects tools (Analyst, Search, custom), executes them, reflects on results, and generates responses. Created as a first-class Snowflake object.", "icon": "smart_toy"},
    {"name": "Tool Orchestration", "description": "The Agent automatically routes questions to the right tool: Cortex Analyst for structured data, Cortex Search for unstructured documents, custom UDFs for business logic.", "icon": "route"},
    {"name": "Custom Tools (UDFs)", "description": "User-defined functions that extend Agent capabilities. The Agent can call any SQL UDF as a tool, enabling custom business logic and calculations.", "icon": "build"},
])


PROMPT_4_1 = """In HIIVE_AI.MARKETPLACE_OPS, create a Cortex Agent called MARKETPLACE_OPS_AGENT that marketplace operations staff can use to ask questions about both structured data and unstructured documents.

It should:
- Use auto as the orchestration model
- Have two tools: the MARKETPLACE_ANALYTICS_VIEW semantic view (for structured data queries) and the marketplace_knowledge_search Cortex Search service (for compliance docs and support tickets)
- Include instructions that define it as the HIIVE Marketplace Operations Assistant, guiding it to:
  - Route structured data questions (volumes, prices, metrics) to the analytics tool
  - Route compliance/regulatory/support questions to the search tool
  - Key domain context: HIIVE is a private securities marketplace for pre-IPO/secondary share trading. ROFR = Right of First Refusal. 409A = fair market value. Accredited investors only.
  - Support English queries
- Include 3-4 sample questions that span both tools (e.g. trade volumes, compliance reviews, pricing trends)

Execute and show confirmation."""

render_prompt("Prompt 4.1", "Create the Cortex Agent", PROMPT_4_1)

render_explanation("What this prompt does", """
Creates a **Cortex Agent** — an AI orchestrator that combines multiple data tools:

**CREATE AGENT anatomy**:

- **MODEL**: The LLM used for orchestration (planning, reflection, response generation). `auto` lets Snowflake select the best available model.

- **TOOLS**: The capabilities the agent can use:
  - **Cortex Search service** (`marketplace_knowledge_search`): For searching compliance reviews, support tickets, and regulatory filings
  - **Semantic view** (`MARKETPLACE_ANALYTICS_VIEW`): For generating SQL queries about trade volumes, pricing, and platform metrics

- **INSTRUCTIONS**: System prompt that shapes behavior, tone, and priorities:
  - Role definition ("You are the HIIVE Marketplace Operations Assistant")
  - Tool routing guidance ("use analytics tool for volumes/prices/metrics")
  - Domain context (ROFR, 409A valuations, accredited investors)
  - Behavioral guidelines (cite sources, flag compliance concerns)

- **SAMPLE_QUESTIONS**: Seed questions shown to users in the UI.

**How the Agent orchestrates**:
1. **Planning**: Receives user question, decides which tool(s) to use
2. **Tool execution**: Calls Analyst (generates + runs SQL) or Search (retrieves documents)
3. **Reflection**: Evaluates tool results — are they sufficient? Need another tool?
4. **Response**: Synthesizes a natural language answer from tool outputs
""")


PROMPT_4_2 = """Test our MARKETPLACE_OPS_AGENT by running queries through SNOWFLAKE.CORTEX.AGENT(). Run these four queries one at a time:

1. Structured data query: "What are the top companies by total trade volume and which sectors dominate?"
2. Unstructured search query: "Have there been any KYC failures or compliance escalations recently? What happened?"
3. Mixed query (should use both tools): "Which companies with the highest trading volume also have compliance concerns flagged?"
4. Trend query: "What is the trend in daily active users over the last quarter?"

For each, show the full response including which tools the agent chose to use."""

render_prompt("Prompt 4.2", "Test the Agent", PROMPT_4_2)

render_explanation("What this prompt does", """
Tests the Agent with four question types that exercise different tool routing:

1. **Pure structured** — routes to Cortex Analyst, generates SQL with GROUP BY company/sector for trade volumes
2. **Pure unstructured** — routes to Cortex Search, retrieves KYC failure and compliance escalation documents
3. **Mixed** — requires BOTH tools: Analyst for trading volume, Search for compliance flags, then combines
4. **Trend analysis** — routes to Analyst for time-series query on platform activity metrics

**What to look for**:
- Which tools did the agent select for each question?
- Did the mixed query correctly use both tools?
- Were the trend results presented clearly with time context?

**Agent vs. RAG**: The RAG pattern in Session 3 was a single retrieve-then-generate pipeline. The Agent is smarter — it can decide to use Search, then Analyst, then Search again based on the question. It splits complex questions into sub-tasks.
""")


PROMPT_4_3 = """In HIIVE_AI.MARKETPLACE_OPS, enhance our agent by adding a custom tool.

1. Create a UDF that calculates trade risk score:

CREATE OR REPLACE FUNCTION HIIVE_AI.MARKETPLACE_OPS.CALCULATE_TRADE_RISK_SCORE(
    company_name VARCHAR,
    trade_value NUMBER,
    shares_pct_of_outstanding NUMBER
)
RETURNS VARIANT
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
                WHEN trade_value > 1000000 AND shares_pct_of_outstanding > 5 THEN 'Large block trade — may trigger ROFR. Require issuer notification and 30-day waiting period. Verify accredited investor status.'
                WHEN trade_value > 500000 OR shares_pct_of_outstanding > 2 THEN 'Elevated trade — enhanced KYC review recommended. Monitor for wash trading patterns.'
                ELSE 'Standard trade — proceed with normal settlement workflow.'
            END
    )
$$;

2. Test the UDF with sample inputs.

3. Recreate MARKETPLACE_OPS_AGENT to include CALCULATE_TRADE_RISK_SCORE as an additional tool alongside the existing Analyst and Search tools.

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
""")


render_key_concepts([
    {"term": "Cortex Agent", "definition": "A first-class Snowflake object that orchestrates LLMs, Cortex Analyst, Cortex Search, and custom tools to answer complex questions. Supports planning, tool use, reflection, and multi-turn conversations."},
    {"term": "Tool Routing", "definition": "The Agent's ability to select the appropriate tool for each question. Structured data -> Analyst, unstructured search -> Search, calculations -> custom UDFs. The LLM decides routing based on the question and tool descriptions."},
    {"term": "Custom Tools", "definition": "SQL UDFs or stored procedures registered as Agent tools. The Agent calls them with extracted parameters. Enables custom business logic, external integrations, and workflow automation."},
    {"term": "Multi-tool Orchestration", "definition": "When a question requires multiple tools (e.g., 'show me trade volume AND compliance concerns'), the Agent plans a sequence of tool calls, executes them, and synthesizes a combined answer."},
])

render_what_you_built([
    "MARKETPLACE_OPS_AGENT — Cortex Agent with Analyst + Search tools",
    "Tested structured, unstructured, mixed, and trend queries",
    "CALCULATE_TRADE_RISK_SCORE UDF as a custom tool",
    "Enhanced agent with three tool types (Analyst + Search + custom)",
])
