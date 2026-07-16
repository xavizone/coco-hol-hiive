import streamlit as st
from components import render_session_header, render_prompt, render_explanation, render_technologies_used, render_key_concepts, render_what_you_built, render_docs_links, render_execution_context

render_session_header(2, "Cortex Analyst & Semantic Views", "10:20 - 10:35 AM", "15 min", "Semantic view with relationships, metrics, and natural language queries")

render_technologies_used([
    {"name": "Cortex Analyst", "description": "Snowflake's text-to-SQL engine that converts natural language questions into SQL queries. Uses a semantic view to understand your data's business meaning, relationships, and metrics.", "icon": "chat"},
    {"name": "Semantic View", "description": "A first-class Snowflake object (CREATE SEMANTIC VIEW) that describes your data in business terms: tables, relationships, facts, dimensions, metrics, and synonyms. The bridge between natural language and SQL.", "icon": "description"},
    {"name": "AI_SQL_GENERATION", "description": "Custom instructions embedded in the semantic view that guide how Cortex Analyst generates SQL — providing domain context, business rules, and disambiguation hints.", "icon": "auto_fix_high"},
])

st.markdown("""
> **Context check:** Before running these prompts, verify your session is using `HIIVE_COCO_HOL_ROLE`, `HIIVE_COCO_HOL_WH`, and `HIIVE_COCO_HOL` database with your personal schema. If anything looks off, run:
> ```sql
> USE ROLE HIIVE_COCO_HOL_ROLE;
> USE WAREHOUSE HIIVE_COCO_HOL_WH;
> USE DATABASE HIIVE_COCO_HOL;
> USE SCHEMA <YOUR_USERNAME>_OPS;
> ```
""")

render_execution_context("cortex_code")

PROMPT_2_1 = """You are a Snowflake Semantic View expert with full knowledge of the latest CREATE SEMANTIC VIEW DDL syntax. In my workshop schema in HIIVE_COCO_HOL, create a semantic view called MARKETPLACE_ANALYTICS_VIEW for use with Cortex Analyst.

The view should cover these 6 tables: COMPANIES, SHAREHOLDERS, LISTINGS, TRADE_EXECUTIONS, PLATFORM_ACTIVITY, USER_SESSIONS.

Requirements:
- Define proper relationships: listings join to companies and shareholders, trade_executions join to listings and companies, platform_activity and user_sessions are standalone time-series tables
- Classify all numeric columns as FACTS (shares, prices, values, percentages, counts) and all categorical/date columns as DIMENSIONS
- Add SYNONYMS on key dimensions where users might use alternate terms (e.g. company_name as 'stock'/'ticker'/'issuer', trade_type as 'transaction'/'deal', listing_type as 'offer'/'ask')
- Define METRICS for key aggregations: total trade volume (SUM), average share price (AVG), total listings (COUNT), average commission (AVG), daily active users (AVG)
- Add descriptive COMMENTs on every table, fact, dimension, and metric
- Include an AI_SQL_GENERATION instruction explaining this is HIIVE marketplace data for pre-IPO secondary trading, defining key terms: ROFR = Right of First Refusal, 409A = IRS fair market value, Accredited investor = SEC qualification

Important DDL rules to follow:
- Clause order must be: TABLES, RELATIONSHIPS, FACTS, DIMENSIONS, METRICS, COMMENT, AI_SQL_GENERATION
- Table references need fully qualified names (DB.SCHEMA.TABLE)
- WITH SYNONYMS must come before COMMENT on individual items
- Metrics must aggregate facts from the same table they are defined on
- AI_SQL_GENERATION goes after COMMENT as a string literal

Execute the SQL, then run DESCRIBE SEMANTIC VIEW and SHOW SEMANTIC VIEWS to confirm it was created with the AI extension active (look for "AI" in the extension column)."""

render_prompt("Prompt 2.1", "Create the Semantic View", PROMPT_2_1)

render_explanation("What this prompt does", """
Creates a **semantic view** — a first-class Snowflake object that enables natural language to SQL.

**Key components**:

| Clause | Purpose | Example |
|--------|---------|---------|
| TABLES | Define logical tables with fully qualified names, PKs | `COMPANIES AS DB.SCHEMA.COMPANIES PRIMARY KEY (COMPANY_ID)` |
| RELATIONSHIPS | Foreign key joins between tables | `LISTINGS (COMPANY_ID) REFERENCES COMPANIES` |
| FACTS | Raw numeric columns for computation | `TRADE_EXECUTIONS.TOTAL_VALUE_USD AS TOTAL_VALUE_USD` |
| DIMENSIONS | Categorical/temporal columns for grouping | `COMPANIES.SECTOR AS SECTOR` |
| METRICS | Pre-defined aggregations | `TRADE_EXECUTIONS.total_vol AS SUM(...)` |
| COMMENT | View-level description | `COMMENT = '...'` |
| AI_SQL_GENERATION | Instructions for Cortex Analyst | `AI_SQL_GENERATION '...'` |

**AI_SQL_GENERATION** is critical — it provides domain context that helps Cortex Analyst disambiguate questions:
```sql
AI_SQL_GENERATION 'This is HIIVE marketplace data for pre-IPO secondary trading.
ROFR = Right of First Refusal. 409A = IRS fair market value.
When asked about trade volume, use SUM(total_value_usd).'
```
Without it, Analyst may misinterpret domain-specific terms or choose wrong aggregation strategies.

**Verifying the view**: After creation, check:
- `SHOW SEMANTIC VIEWS` → the `extension` column should show `["AI"]` confirming AI_SQL_GENERATION is active
- `DESCRIBE SEMANTIC VIEW <name>` → lists all tables, facts, dimensions, metrics, relationships
- In **Snowsight**: Navigate to **Data → Databases → your schema** and find the semantic view. Click it to see the visual editor with warnings/recommendations
""")


PROMPT_2_2 = """Using the MARKETPLACE_ANALYTICS_VIEW in my workshop schema, ask Cortex Analyst these questions:

1. "What are the top 5 companies by total trade volume?"
2. "Which sectors have the most active listings?"
3. "What is the average execution price vs ask price across all trades?"
4. "Show me the daily trading volume trend over the last 6 months"

Show the generated SQL and results for each."""

render_prompt("Prompt 2.2", "Test with Natural Language Queries", PROMPT_2_2)

st.info("""
:material/lightbulb: **Checking your semantic view for warnings and recommendations:**

In **Snowsight**, go to **Data → Databases → HIIVE_COCO_HOL → your schema → MARKETPLACE_ANALYTICS_VIEW**. The semantic view editor shows:
- **Warnings** (yellow): missing comments, unused columns, ambiguous relationships
- **Recommendations** (blue): suggested metrics, additional synonyms, missing dimensions

You can also test queries in the **Cortex Analyst playground**: navigate to **AI & ML → Cortex Analyst** in the left sidebar, select your semantic view, and type natural language questions directly.
""")

render_explanation("What this prompt does", """
Tests Cortex Analyst across different question types:

1. **"Top 5 companies by total trade volume"** — Tests the `total_trade_volume` metric and `company_name` dimension with a JOIN between trade_executions and companies.

2. **"Most active listings by sector"** — Tests filtering on `status` dimension and grouping by `sector` with a JOIN from listings to companies.

3. **"Execution price vs ask price"** — Tests comparison of two facts across tables, requiring a JOIN between trade_executions and listings.

4. **"Daily trading volume trend"** — Tests time-series aggregation on trade_executions with the `trade_date` dimension.

**What to observe**: Look at the generated SQL — does it correctly identify which tables to join, which metrics to use, and how to filter? The `AI_SQL_GENERATION` instruction helps Analyst choose the right approach for domain-specific questions.
""")


PROMPT_2_3 = """Now expand our MARKETPLACE_ANALYTICS_VIEW semantic view to also include the PRICING_SIGNALS table.

You are a semantic view expert. Follow these steps:
1. Query INFORMATION_SCHEMA.COLUMNS to discover the full schema of PRICING_SIGNALS
2. Recreate MARKETPLACE_ANALYTICS_VIEW with CREATE OR REPLACE, keeping all original definitions and adding PRICING_SIGNALS:
   - Add it to TABLES with its primary key
   - Add a RELATIONSHIP to COMPANIES via company_id
   - Classify its columns as FACTS (numeric: price_per_share, confidence_score, price_change_pct) and DIMENSIONS (categorical/date: signal_type with synonym 'valuation source', signal_date, source)
   - Add METRICS: avg_price_change (AVG of price_change_pct), valuation_signal_count (COUNT of signal_id)
   - Keep the existing AI_SQL_GENERATION instruction and append context about pricing signals

3. After creation, verify:
   - Run DESCRIBE SEMANTIC VIEW to confirm PRICING_SIGNALS appears
   - Run SHOW SEMANTIC VIEWS to confirm the AI extension is still active
   - Test by asking: "Which companies have the highest price volatility based on pricing signals and what are the signal sources?"

Execute all SQL and show results."""

render_prompt("Prompt 2.3", "Expand the Semantic View", PROMPT_2_3)

render_explanation("What this prompt does", """
Demonstrates the **iterative semantic view development cycle**: expand the view, then immediately test.

**The expansion pattern**:
1. Discover the table schema via INFORMATION_SCHEMA
2. Recreate the view with CREATE OR REPLACE (must include ALL original definitions — it's a full replacement)
3. Add the new table, relationship, facts, dimensions, metrics
4. Verify and test

**Key insight**: A semantic view is only as good as the tables and definitions it contains. When users ask about price volatility but PRICING_SIGNALS isn't defined in the view, Analyst can't help. After expansion, it can.

**Metric granularity rule**: Metrics must be defined on the table whose facts they aggregate:
```sql
-- Correct: metric on PRICING_SIGNALS aggregates PRICING_SIGNALS facts
PRICING_SIGNALS.avg_price_change AS AVG(PRICING_SIGNALS.PRICE_CHANGE_PCT)

-- Wrong: metric on COMPANIES cannot aggregate PRICING_SIGNALS facts directly
COMPANIES.avg_price_change AS AVG(PRICING_SIGNALS.PRICE_CHANGE_PCT)  -- ERROR
```

**Checking for warnings**: After expanding, revisit the view in Snowsight's visual editor. New columns may trigger recommendations for additional dimensions or metrics you missed.
""")


render_key_concepts([
    {"term": "Cortex Analyst", "definition": "Snowflake's text-to-SQL engine. Takes natural language questions and generates SQL queries using a semantic view for context. Supports aggregations, joins, filtering, and time-series analysis."},
    {"term": "Semantic View", "definition": "A first-class Snowflake object (CREATE SEMANTIC VIEW) that maps database tables to business concepts. Contains table definitions, relationships, facts, dimensions, metrics, synonyms, and AI instructions."},
    {"term": "AI_SQL_GENERATION", "definition": "Custom instructions embedded in the semantic view (after COMMENT) that guide how Cortex Analyst generates SQL. Provides domain-specific context, term definitions, and disambiguation hints. Critical for domain-specific accuracy."},
    {"term": "Fact vs Dimension vs Metric", "definition": "Facts are raw numeric columns (total_value_usd). Dimensions are categorical/temporal columns for grouping and filtering (company_name, trade_date). Metrics are pre-defined aggregations over facts (SUM(total_value_usd), AVG(commission_pct))."},
    {"term": "Validation & Warnings", "definition": "Snowflake validates semantic views at creation time. Check warnings in the Snowsight visual editor (Data → your schema → the view) or via SHOW SEMANTIC VIEWS (extension column shows active AI features)."},
])

render_docs_links([
    {"title": "Semantic Views", "url": "https://docs.snowflake.com/en/sql-reference/sql/create-semantic-view"},
    {"title": "Cortex Analyst", "url": "https://docs.snowflake.com/en/user-guide/snowflake-cortex/cortex-analyst"},
    {"title": "AI_SQL_GENERATION", "url": "https://docs.snowflake.com/en/sql-reference/sql/create-semantic-view#ai-sql-generation"},
    {"title": "Semantic View Best Practices", "url": "https://docs.snowflake.com/en/user-guide/snowflake-cortex/cortex-analyst/semantic-view-best-practices"},
])

render_what_you_built([
    "MARKETPLACE_ANALYTICS_VIEW semantic view with 6 core tables, relationships, and AI_SQL_GENERATION",
    "Natural language queries testing trade volume, listings, pricing, and trends",
    "Expanded view with PRICING_SIGNALS table and valuation metrics (7 tables total)",
    "Iterative semantic view development and validation pattern",
])


# --- Bonus Reading ---
with st.expander("Bonus Reading: Semantic Views as Your Single Source of Truth", expanded=False):
    st.markdown("""
## The Semantic View Lifecycle

A semantic view isn't a one-time setup — it's a living artifact that evolves with your data and serves as the **single source of truth** for how your organization understands its data.

---

### Verified Queries: Teaching Analyst by Example

**What they are**: Verified queries are question-SQL pairs embedded directly in the semantic view that serve as "golden examples" for Cortex Analyst.

**Why they matter**: For complex or ambiguous questions, Analyst can match incoming questions to verified examples and reuse the known-good SQL pattern rather than generating from scratch.

**How to add them (DDL)**:
```sql
CREATE OR REPLACE SEMANTIC VIEW my_view
  ...
  AI_VERIFIED_QUERIES (
    top_traders AS (
      QUESTION 'Who are the top traders by volume?'
      SQL 'SELECT c.COMPANY_NAME, SUM(t.TOTAL_VALUE_USD) as vol
           FROM TRADE_EXECUTIONS t JOIN COMPANIES c
           ON t.COMPANY_ID = c.COMPANY_ID
           GROUP BY 1 ORDER BY 2 DESC LIMIT 10'
    ),
    monthly_trend AS (
      QUESTION 'Show monthly trading trends'
      SQL 'SELECT DATE_TRUNC(''MONTH'', TRADE_DATE) as month,
           SUM(TOTAL_VALUE_USD) as volume
           FROM TRADE_EXECUTIONS GROUP BY 1 ORDER BY 1'
    )
  )
  ...;
```

**How to add them in Snowsight**: In the Cortex Analyst playground, after running a question and verifying the SQL is correct, click **"Verify"** to save it as a verified query directly to the semantic view.

---

### Snowsight Visual Editor: Monitoring & Suggestions

Navigate to **Data → Databases → your schema → your semantic view** in Snowsight to access the visual editor. Here you can:

| Feature | What it does |
|---------|-------------|
| **Warnings** (yellow badges) | Flags issues: missing comments, unused columns, ambiguous join paths |
| **Suggestions** (blue badges) | Recommends: new dimensions for uncovered columns, additional metrics, missing synonyms |
| **Accept/Dismiss** | One-click to add suggested definitions or dismiss them |
| **Usage stats** | Shows which dimensions/metrics are actually queried by Analyst |
| **Edit inline** | Modify comments, synonyms, and metric expressions without writing DDL |

**Best practice**: After initial creation, check the editor for suggestions. Snowflake analyzes your table schemas and recommends definitions you may have missed. Accept the ones that make sense, dismiss the rest.

---

### Keeping the Model Up to Date

Semantic views automatically reflect schema changes in underlying tables:
- **New columns** added to base tables appear as suggestions in the visual editor
- **Dropped columns** trigger validation warnings (fix by removing the stale definition)
- **Data type changes** are detected at query time

For **proactive maintenance**:
- Review the view monthly or when data models change
- Use `DESCRIBE SEMANTIC VIEW` to audit current definitions
- Use `SYSTEM$READ_YAML_FROM_SEMANTIC_VIEW('view_name')` to export the full spec for version control
- Store the YAML in git alongside your dbt models or migration scripts

---

### Semantic View as the Universal Data Contract

The semantic view becomes the **single source of truth** across your entire tool ecosystem:

```
┌─────────────────────────────────────────────────┐
│           SEMANTIC VIEW (Source of Truth)         │
│  Tables • Relationships • Facts • Dimensions     │
│  Metrics • Synonyms • AI Instructions            │
└────────┬────────────┬────────────┬───────────────┘
         │            │            │
    ┌────▼────┐  ┌────▼────┐  ┌───▼────────┐
    │ Cortex  │  │  dbt    │  │ External   │
    │ Analyst │  │ Models  │  │ AI Tools   │
    │ (NL→SQL)│  │ (ELT)  │  │(Claude,etc)│
    └─────────┘  └─────────┘  └────────────┘
```

**Who benefits**:

- **Cortex Analyst** — Uses the semantic view directly for text-to-SQL generation
- **dbt** — Can reference the same business definitions (metric names, grain, relationships) ensuring transformation logic matches the semantic layer
- **External AI tools (Claude, GPT, etc.)** — Can consume the YAML spec via `SYSTEM$READ_YAML_FROM_SEMANTIC_VIEW()` to understand your data model and generate correct queries
- **BI tools** — Metrics defined once in the semantic view mean consistent KPIs regardless of which dashboard tool queries the data
- **Data governance** — Comments, synonyms, and relationships provide a discoverable, auditable business glossary

**The key insight**: Instead of each tool maintaining its own understanding of "what does total_trade_volume mean?" or "how do listings relate to companies?", the semantic view defines it once and every consumer inherits the same truth.

---

### Exporting for Version Control

```sql
-- Export as YAML for git
SELECT SYSTEM$READ_YAML_FROM_SEMANTIC_VIEW('MARKETPLACE_ANALYTICS_VIEW');

-- Recreate from YAML (CI/CD deployments)
CALL SYSTEM$CREATE_SEMANTIC_VIEW_FROM_YAML(
  'MARKETPLACE_ANALYTICS_VIEW',
  $$<yaml_content>$$
);
```

This enables a **GitOps workflow**: edit YAML in your repo, review in PRs, deploy via CI/CD — just like dbt models.
""")
