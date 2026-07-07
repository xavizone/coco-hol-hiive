import streamlit as st
from components import render_session_header, render_prompt, render_explanation, render_technologies_used, render_key_concepts, render_what_you_built

render_session_header(2, "Cortex Analyst & Semantic Views", "10:25 - 10:55 AM", "30 min", "Semantic view with relationships, metrics, and natural language queries")

render_technologies_used([
    {"name": "Cortex Analyst", "description": "Snowflake's text-to-SQL engine that converts natural language questions into SQL queries. Uses a semantic view to understand your data's business meaning, relationships, and metrics.", "icon": "chat"},
    {"name": "Semantic View", "description": "A first-class Snowflake object (CREATE SEMANTIC VIEW) that describes your data in business terms: tables, relationships, facts, dimensions, metrics, and synonyms. The bridge between natural language and SQL.", "icon": "description"},
    {"name": "AI_SQL_GENERATION", "description": "Custom instructions embedded in the semantic view that guide how Cortex Analyst generates SQL — providing domain context, business rules, and disambiguation hints.", "icon": "auto_fix_high"},
])


PROMPT_2_1 = """In HIIVE_AI.MARKETPLACE_OPS, create a semantic view called MARKETPLACE_ANALYTICS_VIEW for use with Cortex Analyst. It should cover these tables: COMPANIES, SHAREHOLDERS, LISTINGS, TRADE_EXECUTIONS, PRICING_SIGNALS, PLATFORM_ACTIVITY, USER_SESSIONS.

Include:
- Proper relationships between the tables (listings join to companies via company_id, listings join to shareholders via shareholder_id, trade_executions join to listings via listing_id, trade_executions join to companies via company_id, pricing_signals join to companies via company_id, platform_activity is standalone time-series, user_sessions is standalone time-series)
- Facts for all key numeric columns: shares_offered, ask_price_per_share, shares_traded, execution_price_per_share, total_value_usd, commission_pct, active_users, page_views, bids_placed, matches_made, price_per_share, confidence_score, price_change_pct
- Dimensions for categorical columns like company_name, sector, funding_stage, shareholder_type, listing_type, status, trade_type, compliance_status, signal_type, platform_section, device_type, user_type, referral_source, and all date/time columns
- Add useful SYNONYMS on dimensions where users might use different terms (e.g. company_name could also be called 'stock', 'ticker', or 'issuer'; trade_type could be 'transaction' or 'deal'; listing_type could be 'offer' or 'ask')
- Metrics with pre-aggregated calculations: total_trade_volume (SUM of total_value_usd), avg_share_price (AVG of execution_price_per_share), listing_fill_rate (shares_traded/shares_offered), total_listings (COUNT), avg_commission (AVG of commission_pct), daily_active_users (AVG of active_users)
- Descriptive COMMENTs on every table, fact, dimension, and metric explaining the business meaning
- An AI_SQL_GENERATION instruction that provides domain context: this is HIIVE marketplace data for pre-IPO secondary trading. ROFR = Right of First Refusal. 409A = IRS fair market value. Accredited investor = SEC qualification. Key companies include Stripe, SpaceX, Databricks etc.

Execute the SQL and confirm with DESCRIBE SEMANTIC VIEW."""

render_prompt("Prompt 2.1", "Create the Semantic View", PROMPT_2_1)

render_explanation("What this prompt does", """
Creates a **semantic view** — a first-class Snowflake object that enables natural language to SQL:

**Key components of a semantic view**:

- **TABLES**: Logical tables with aliases, primary keys, and comments
- **RELATIONSHIPS**: Foreign key joins between tables (e.g., listings -> companies)
- **FACTS**: Raw numeric columns available for computation (shares_offered, total_value_usd)
- **DIMENSIONS**: Categorical and temporal columns for grouping/filtering, with optional synonyms
- **METRICS**: Pre-defined aggregations (SUM, AVG, COUNT) that Cortex Analyst can use directly
- **AI_SQL_GENERATION**: Custom instructions that guide how Analyst generates SQL

**Synonyms** help Cortex Analyst understand different ways users refer to the same concept:
```sql
c.company_name ... WITH SYNONYMS = ('stock', 'ticker', 'issuer')
```

**Facts vs Metrics**:
- Facts are raw columns (e.g., `total_value_usd`) — building blocks
- Metrics are pre-defined aggregations (e.g., `SUM(total_value_usd)`) — ready-to-use calculations
""")


PROMPT_2_2 = """Ask Cortex Analyst these questions using HIIVE_AI.MARKETPLACE_OPS.MARKETPLACE_ANALYTICS_VIEW:

1. "What are the top 5 companies by total trade volume?"
2. "Which sectors have the most active listings?"
3. "What is the average execution price vs ask price across all trades?"
4. "Show me the daily trading volume trend over the last 6 months"

Show the generated SQL and results for each."""

render_prompt("Prompt 2.2", "Test with Natural Language Queries", PROMPT_2_2)

st.info("""
:material/lightbulb: **You can also test these in the Cortex Analyst UI!**

In Snowsight, navigate to **AI & ML → Cortex Analyst** in the left sidebar. Select your `MARKETPLACE_ANALYTICS_VIEW` semantic view, and you'll see a playground where you can type natural language questions and see the generated SQL and results interactively. Try pasting the questions above directly into that playground.
""")

render_explanation("What this prompt does", """
Tests Cortex Analyst across different question types:

1. **"Top 5 companies by total trade volume"** — Tests the `total_trade_volume` metric and `company_name` dimension with a JOIN between trade_executions and companies.

2. **"Most active listings by sector"** — Tests filtering on `status` dimension and grouping by `sector` with a JOIN from listings to companies.

3. **"Execution price vs ask price"** — Tests comparison of two facts across tables, requiring a JOIN between trade_executions and listings.

4. **"Daily trading volume trend"** — Tests time-series aggregation on trade_executions with a date dimension.

**What to observe**: Look at the generated SQL — does it correctly identify which tables to join, which metrics to use, and how to filter? This demonstrates the power of the semantic layer.
""")


PROMPT_2_3 = """Now expand our MARKETPLACE_ANALYTICS_VIEW semantic view in HIIVE_AI.MARKETPLACE_OPS to also include the PRICING_SIGNALS table with proper relationships and definitions.

1. Query INFORMATION_SCHEMA.COLUMNS to get the full schema of PRICING_SIGNALS
2. Recreate MARKETPLACE_ANALYTICS_VIEW with all original definitions plus PRICING_SIGNALS enhancements, adding:
   - Relationship to COMPANIES via company_id (already exists, ensure it's included)
   - Facts: price_per_share, confidence_score, price_change_pct
   - Dimensions: signal_type (with synonym 'valuation source'), company_name, signal_date
   - Metrics: avg_price_change (AVG of price_change_pct), valuation_signal_count (COUNT of signals)
   - Appropriate comments

3. Test the expanded view by asking: "Which companies have the highest price volatility based on pricing signals and what are the signal sources?"

Execute all SQL and show the result."""

render_prompt("Prompt 2.3", "Expand the Semantic View", PROMPT_2_3)

render_explanation("What this prompt does", """
Demonstrates the **iterative semantic view development cycle**: expand the view, then immediately test.

**The expansion pattern**:
1. Check what columns exist in the new table via INFORMATION_SCHEMA
2. Recreate the view with CREATE OR REPLACE SEMANTIC VIEW
3. Add the new table, relationship, facts, dimensions, metrics
4. Test to confirm Analyst can now answer questions about pricing signals

**Key insight**: A semantic view is only as good as the tables and definitions it contains. When users ask about price volatility but PRICING_SIGNALS isn't fully defined in the view, Analyst can't help. After expansion, it can.

**The avg_price_change metric** is interesting because it captures valuation movement:
```sql
METRIC avg_price_change = AVG(price_change_pct)
```
Combined with `valuation_signal_count`, this lets analysts understand both the direction and confidence of pricing data.
""")


render_key_concepts([
    {"term": "Cortex Analyst", "definition": "Snowflake's text-to-SQL engine. Takes natural language questions and generates SQL queries using a semantic view for context. Supports aggregations, joins, filtering, and time-series analysis."},
    {"term": "Semantic View", "definition": "A first-class Snowflake object (CREATE SEMANTIC VIEW) that maps database tables to business concepts. Contains table definitions, relationships, facts, dimensions, metrics, synonyms, and AI instructions."},
    {"term": "Fact vs Dimension vs Metric", "definition": "Facts are raw numeric columns (total_value_usd). Dimensions are categorical/temporal columns for grouping and filtering (company_name, trade_date). Metrics are pre-defined aggregations over facts (SUM(total_value_usd), AVG(commission_pct))."},
    {"term": "AI_SQL_GENERATION", "definition": "Custom instructions embedded in the semantic view that guide SQL generation. Use this to provide domain-specific context, business rules, and disambiguation hints."},
])

render_what_you_built([
    "MARKETPLACE_ANALYTICS_VIEW semantic view with 7 tables and relationships",
    "Natural language queries testing trade volume, listings, pricing, and trends",
    "Expanded view with PRICING_SIGNALS and valuation metrics",
    "Iterative semantic view development pattern",
])
