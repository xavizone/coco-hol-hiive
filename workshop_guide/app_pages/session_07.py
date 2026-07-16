import streamlit as st
from components import render_session_header, render_prompt, render_explanation, render_technologies_used, render_key_concepts, render_what_you_built, render_docs_links, render_execution_context

render_session_header(7, "DMF & Monitoring", "11:10 - 11:25 AM", "15 min", "Data Metric Functions, scheduled monitoring, and alerts for anomaly detection")

render_technologies_used([
    {"name": "Data Metric Functions (DMFs)", "description": "Snowflake's native data quality framework. SQL functions that compute metrics over tables on a schedule. Built-in system DMFs for common checks plus custom DMFs for business logic.", "icon": "monitoring"},
    {"name": "DMF Scheduling", "description": "CRON-based scheduling that runs DMFs automatically. Results stored in EVENT_TABLE for querying and alerting.", "icon": "schedule"},
    {"name": "Snowflake Alerts", "description": "Event-driven automation triggered by conditions (like DMF threshold breaches). Can send notifications or execute corrective actions.", "icon": "notification_important"},
])

st.warning("""
:material/warning: **Enterprise Edition Required**

Data Metric Functions (DMFs) require **Snowflake Enterprise Edition** or higher. HIIVE's current account is on **Standard Edition**, which means DMFs cannot be executed directly in this lab.

**What this means for today:**
- The Snowflake team will **live-demo** this section so you can see DMFs in action
- Follow along with the concepts — this is exactly what your monitoring could look like after an edition discussion
- The prompts below are provided for reference and future use

**Why DMFs matter for HIIVE:** Your current monitoring stack (dbt Elementary + Datadog) is reactive — it catches issues only when dbt runs. DMFs provide continuous, scheduled monitoring that detects anomalies BETWEEN dbt runs. This is the proactive monitoring gap your team identified.
""")

render_execution_context("cortex_code")


PROMPT_7_1 = """Set up Data Metric Functions for continuous monitoring of our critical marketplace tables.

I need you to:
1. Configure an event table in my schema to store DMF results
2. Apply built-in system DMFs to these tables:
   - TRADE_EXECUTIONS: check for NULLs in compliance_status, track row count, and monitor freshness
   - LISTINGS: check for NULLs in ask_price_per_share and track row count
   - COMPLIANCE_REVIEWS: track row count and monitor freshness
3. Schedule them on a 2-minute CRON interval so we can see results during this session (use 'USING CRON */2 * * * * America/Vancouver')
4. Also insert a test row into TRADE_EXECUTIONS to trigger an immediate evaluation — something like trade_id='DMF_TEST_001', with today's date, a NULL compliance_status, and reasonable values for the other columns
5. Verify the DMF references are active by querying INFORMATION_SCHEMA.DATA_METRIC_FUNCTION_REFERENCES

Execute everything and show me what's attached. We should see DMF results in the event table within 2 minutes."""

render_prompt("Prompt 7.1", "Create System DMFs for Critical Tables", PROMPT_7_1)

render_explanation("What this prompt does", """
Sets up Snowflake's built-in Data Metric Functions on your most critical tables:

```sql
-- Configure where DMF results are stored
ALTER DATABASE HIIVE_COCO_HOL SET DATA_METRIC_SCHEDULE_EVENT_TABLE = 'HIIVE_COCO_HOL.<username>_OPS.DMF_EVENTS';

-- Apply system DMFs to TRADE_EXECUTIONS
ALTER TABLE TRADE_EXECUTIONS ADD DATA METRIC FUNCTION SNOWFLAKE.CORE.NULL_COUNT ON (compliance_status);
ALTER TABLE TRADE_EXECUTIONS ADD DATA METRIC FUNCTION SNOWFLAKE.CORE.ROW_COUNT ON ();
ALTER TABLE TRADE_EXECUTIONS ADD DATA METRIC FUNCTION SNOWFLAKE.CORE.FRESHNESS ON ();

-- Schedule on 2-minute CRON (so we see results during the lab)
ALTER TABLE TRADE_EXECUTIONS SET DATA_METRIC_SCHEDULE = 'USING CRON */2 * * * * America/Vancouver';

-- Insert a test row to also trigger immediate evaluation
INSERT INTO TRADE_EXECUTIONS (trade_id, trade_date, compliance_status, ...)
  VALUES ('DMF_TEST_001', CURRENT_DATE(), NULL, ...);
```

**Why 2-minute CRON instead of TRIGGER_ON_CHANGES?** In production you'd use TRIGGER_ON_CHANGES so DMFs fire only when data arrives (cheaper). But for a live lab, a short CRON ensures we see results in the UI within 2 minutes — regardless of whether new data lands.

**Why the test INSERT?** The NULL compliance_status will show up in NULL_COUNT, the new row bumps ROW_COUNT, and FRESHNESS resets to "just now." This gives us immediate proof the DMFs are working.

**System DMFs available**: NULL_COUNT, DUPLICATE_COUNT, ROW_COUNT, FRESHNESS, UNIQUE_COUNT. These cover the most common data quality checks without any custom code.
""")


PROMPT_7_2 = """Now create three custom Data Metric Functions for anomaly detection specific to our marketplace.

I need:

1. A trade volume anomaly DMF called trade_volume_anomaly_check that:
   - Takes a table argument with total_value_usd and trade_date columns
   - Compares today's trade volume against the 30-day rolling average
   - Returns 1 if volume is more than 2 standard deviations above average (spike), -1 if below (drop), 0 if normal

2. A pricing deviation DMF called pricing_deviation_check that:
   - Takes a table argument with execution_price_per_share and company_id columns
   - Cross-references against the latest 409A valuation in PRICING_SIGNALS
   - Returns the count of trades executing at more than 20% below the latest 409A price

3. A compliance backlog DMF called compliance_backlog_check that:
   - Takes a table argument with outcome and review_date columns
   - Counts reviews with status 'escalated' or 'conditionally_approved' that are older than 7 days
   - Returns that count (0 = healthy, >0 = backlog building)

4. Apply all three custom DMFs to the appropriate tables

Execute everything and confirm they're attached."""

render_prompt("Prompt 7.2", "Create Custom DMFs for Anomaly Detection", PROMPT_7_2)

render_explanation("What this prompt does", """
Creates business-specific anomaly detection that goes far beyond generic null checks:

- **trade_volume_anomaly_check**: Statistical anomaly detection using rolling 30-day window. Returns 1 (spike), -1 (drop), or 0 (normal).
- **pricing_deviation_check**: Cross-references trade prices against 409A valuations. Flags regulatory risk.
- **compliance_backlog_check**: Monitors review aging. Catches operational bottlenecks before they become compliance issues.

**Why this matters for HIIVE**: Your current dbt Elementary setup only runs when dbt runs (GitHub Actions). These DMFs run continuously on Snowflake's schedule — catching issues BETWEEN dbt runs.
""")


PROMPT_7_3 = """Now set up alerting so DMF anomalies trigger notifications automatically.

I need you to:
1. Query the most recent 20 DMF results from my event table — show me the metric name, table name, value, and measurement time
2. Create an alert called trade_volume_alert that:
   - Runs every hour (CRON schedule, America/Vancouver timezone)
   - Uses the HIIVE_COCO_HOL_WH warehouse
   - Checks if any trade_volume_anomaly_check measurement in the last hour returned a non-zero value
   - If triggered, sends an email to data-team@hiive.com with subject "ALERT: Trade Volume Anomaly Detected"
3. Resume the alert so it starts running
4. Show me a query that summarizes historical DMF trends — group by metric, table, value, and hour so we can see patterns over time

Execute everything and explain how this compares to what we'd get from dbt Elementary."""

render_prompt("Prompt 7.3", "Schedule DMFs and Create Alerts", PROMPT_7_3)

render_explanation("What this prompt does", """
Closes the loop from detection to notification:

```sql
CREATE OR REPLACE ALERT trade_volume_alert
  WAREHOUSE = HIIVE_COCO_HOL_WH
  SCHEDULE = 'USING CRON 0 * * * * America/Vancouver'
  IF (EXISTS (...))
  THEN CALL SYSTEM$SEND_EMAIL(...);
```

**DMFs vs dbt Elementary — complementary, not competing**:

| Aspect | dbt Elementary | Snowflake DMFs |
|--------|---------------|----------------|
| **Runs when** | dbt runs (GitHub Actions) | Snowflake schedule (independent) |
| **Catches issues** | At build time | Between builds |
| **Alert mechanism** | Slack via dbt hooks | Email, webhook, or custom action |
| **Statistical checks** | Limited | Custom SQL (rolling averages, stddev) |
| **Best for** | Schema validation, row counts | Continuous anomaly detection |

**Position**: Keep dbt Elementary for schema/logic validation. Add DMFs for the gap — continuous monitoring that doesn't depend on GitHub Actions reliability.
""")


st.info("""
:material/monitor_heart: **Verify DMFs in the Snowsight UI**

After running the prompts above, you can view and manage your DMFs directly in Snowsight:

1. **Data Quality tab** — Navigate to **Monitoring → Data Quality** in the left sidebar. You'll see all active DMF schedules, recent results, and any anomaly flags across your tables.

2. **Table-level DMF view** — Browse to any table (e.g., `HIIVE_COCO_HOL → <your_schema> → TRADE_EXECUTIONS`), then click the **Data Quality** tab on the table detail page. This shows all DMFs attached to that specific table with their latest metric values and history charts.

3. **Alerts monitoring** — Navigate to **Monitoring → Alerts** in the left sidebar to see your `trade_volume_alert`. You can view execution history, check if it has fired, and manually suspend/resume it.

4. **Event table results** — The DMF_EVENTS table in your schema stores all historical measurements. You can query it directly or view it in the Data Preview tab to see raw metric values and timestamps.

**What to look for in the UI:**
- Green checkmarks = DMF passed (value within threshold)
- Red/yellow indicators = DMF flagged an anomaly
- History charts show metric trends over time — useful for spotting gradual drift vs sudden spikes
""")

render_docs_links([
    {"title": "Data Metric Functions", "url": "https://docs.snowflake.com/en/user-guide/data-quality-intro"},
    {"title": "System DMFs", "url": "https://docs.snowflake.com/en/sql-reference/data-metric-functions/system-dmf-reference"},
    {"title": "CREATE DATA METRIC FUNCTION", "url": "https://docs.snowflake.com/en/sql-reference/sql/create-data-metric-function"},
    {"title": "DMF Scheduling", "url": "https://docs.snowflake.com/en/user-guide/data-quality-working"},
    {"title": "Snowflake Alerts", "url": "https://docs.snowflake.com/en/user-guide/alerts"},
])

render_key_concepts([
    {"term": "Data Metric Function (DMF)", "definition": "A Snowflake UDF-like function specifically designed to measure data quality metrics. Can be system-provided (NULL_COUNT, FRESHNESS, ROW_COUNT, DUPLICATE_COUNT, UNIQUE_COUNT) or custom-built for business logic. DMFs are attached to tables and run on a schedule."},
    {"term": "DMF Scheduling", "definition": "DMFs can run on CRON schedules or TRIGGER_ON_CHANGES. Results are stored in the database's event table for historical analysis, trend detection, and alerting."},
    {"term": "Anomaly Detection Pattern", "definition": "Custom DMFs that compute statistical thresholds (rolling averages, standard deviations) and flag deviations automatically. Returns numeric codes (1 = spike, -1 = drop, 0 = normal) for easy alerting."},
    {"term": "DMFs vs dbt Tests", "definition": "dbt tests validate at build time — they run when dbt runs. DMFs monitor continuously, catching issues between runs. They're complementary: dbt for schema/logic validation, DMFs for ongoing anomaly detection."},
])

render_what_you_built([
    "System DMFs on TRADE_EXECUTIONS, LISTINGS, COMPLIANCE_REVIEWS",
    "Custom DMF: trade_volume_anomaly_check (statistical anomaly detection)",
    "Custom DMF: pricing_deviation_check (regulatory risk flagging)",
    "Custom DMF: compliance_backlog_check (operational bottleneck detection)",
    "Scheduled monitoring with TRIGGER_ON_CHANGES execution",
    "Alert: trade_volume_alert with hourly check and email notification",
    "Historical DMF event analysis queries",
])


# ─────────────────────────────────────────────────────────────────────────────
# Bonus: Real-World DMF Applications
# ─────────────────────────────────────────────────────────────────────────────

st.markdown("---")
st.markdown("## :material/lightbulb: Bonus: Real-World DMF Applications")

st.markdown("""
DMFs are more than a data quality checkbox — they're a **continuous observability layer** that gives different teams real-time visibility into data health without writing pipelines or dashboards.
""")

with st.expander("**Financial Services & Compliance**", expanded=True):
    st.markdown("""
**Real-world examples:**
- **Transaction monitoring**: A DMF that counts transactions exceeding regulatory thresholds (e.g., $10K AML reporting limits) and alerts compliance teams before end-of-day reporting
- **Settlement reconciliation**: Compare expected vs actual settlement counts daily — a mismatch of even 1 row could indicate a failed trade
- **Regulatory filing completeness**: Track whether all required fields are populated before submission deadlines (e.g., SEC filings with NULL beneficial owner = regulatory risk)

**Why it matters:** Manual spot-checks miss issues between review cycles. A DMF running every 5 minutes catches a data gap within minutes of it appearing — not days later when an auditor flags it.
""")

with st.expander("**Data Engineering Teams**"):
    st.markdown("""
**Real-world examples:**
- **Pipeline freshness SLAs**: FRESHNESS DMF on critical tables ensures upstream pipelines delivered on time. If your marketing attribution table hasn't refreshed in 4 hours, the campaign team is making decisions on stale data.
- **Schema drift detection**: DUPLICATE_COUNT on primary key columns catches accidental fan-out from a bad JOIN in an upstream model
- **Volume anomaly detection**: ROW_COUNT compared to historical patterns catches both silent failures (0 new rows = pipeline broke) and data explosions (10x normal = cartesian join upstream)
- **Cross-system reconciliation**: Custom DMF comparing row counts between a raw ingestion table and its downstream cleaned version — delta > 5% triggers investigation

**Pro tip:** Use `TRIGGER_ON_CHANGES` in production instead of CRON. It only runs when data actually changes, saving compute costs while still catching issues immediately.
""")

with st.expander("**Analytics & BI Teams**"):
    st.markdown("""
**Real-world examples:**
- **Dashboard data freshness**: Before stakeholders open their morning dashboard, a FRESHNESS DMF ensures the underlying tables were updated overnight. If not, an alert fires and the dashboard shows a "data delayed" banner.
- **Metric consistency checks**: A custom DMF that validates total revenue in the fact table matches the sum of line items — catches rounding errors or missing records that would show wrong numbers in executive reports
- **Dimension table integrity**: NULL_COUNT on key dimension attributes (customer segment, region, product category) prevents "Unknown" slices from growing silently in reports

**Why it matters:** BI teams often discover data issues when a VP asks "why does this number look wrong?" DMFs shift that discovery from reactive (embarrassing) to proactive (professional).
""")

with st.expander("**Product & Operations Teams**"):
    st.markdown("""
**Real-world examples:**
- **User activity monitoring**: A DMF tracking daily active user counts — a sudden 30% drop could indicate a broken login flow, not just "slow week"
- **Feature adoption tracking**: Count of NULL values in a new feature's tracking column shows whether instrumentation is working correctly
- **SLA monitoring**: Custom DMF that counts support tickets older than the SLA window (e.g., 24 hours for P1 tickets) — directly ties data quality to operational commitments
- **Inventory/supply chain**: Track when stock levels in the data warehouse diverge from the source system by more than a threshold — catches sync failures before they cause stockouts
""")

with st.expander("**Advanced DMF Patterns**"):
    st.markdown("""
**Beyond basic checks — patterns that unlock real value:**

| Pattern | How it works | Use case |
|---------|-------------|----------|
| **Statistical process control** | Compare metric to rolling mean ± N standard deviations | Detect gradual drift vs sudden breaks |
| **Cross-table referential integrity** | DMF on table A that queries table B for orphan records | Catch broken foreign keys without constraints |
| **Temporal gap detection** | Check for missing time intervals in time-series data | Ensure no hours/days are silently dropped |
| **Distribution shift detection** | Compare value percentiles to historical baselines | Catch upstream schema changes that shift data semantics |
| **Conditional freshness** | Different freshness thresholds by partition (e.g., region) | "US data must be < 1hr old, APAC < 4hr" |
| **Cascading alerts** | Alert escalates severity if metric stays anomalous for N consecutive runs | Distinguish transient blips from real incidents |

**Combining DMFs with Snowflake Alerts creates a full observability stack:**
1. **DMFs** detect the issue (measurement)
2. **Alerts** notify the right team (routing)
3. **Event table history** provides context (investigation)
4. **Dashboards** on DMF results show trends (visibility)

This replaces expensive third-party data observability tools (Monte Carlo, Anomalo, etc.) with native Snowflake capabilities — no additional infrastructure, no data leaving your account, and no separate billing.
""")

with st.expander("**Who benefits from DMF metrics?**"):
    st.markdown("""
| Team | What they monitor | Business impact |
|------|------------------|-----------------|
| **Data Engineering** | Pipeline freshness, row counts, schema drift | Catch failures before downstream consumers notice |
| **Analytics/BI** | Metric consistency, dimension completeness | Prevent wrong numbers in executive dashboards |
| **Compliance/Legal** | Regulatory field completeness, threshold breaches | Avoid fines and audit findings |
| **Product** | Feature instrumentation, user activity patterns | Distinguish data bugs from real product issues |
| **Operations** | SLA adherence, backlog growth, queue depths | Proactive intervention before customers are impacted |
| **Finance** | Revenue reconciliation, transaction completeness | Accurate books and faster close cycles |
| **Security** | Access pattern anomalies, unusual query volumes | Early indicator of data exfiltration or misuse |

**The key insight:** DMFs make data quality a **shared responsibility** with **shared visibility**. Instead of data engineers discovering issues in isolation, every team can subscribe to the metrics that matter to them — and trust that the data behind their decisions is continuously validated.
""")
