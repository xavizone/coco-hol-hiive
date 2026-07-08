import streamlit as st
from components import render_session_header, render_prompt, render_explanation, render_technologies_used, render_key_concepts, render_what_you_built

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


PROMPT_7_1 = """Set up Data Metric Functions for continuous monitoring of our critical marketplace tables.

I need you to:
1. Configure an event table in my schema to store DMF results
2. Apply built-in system DMFs to these tables:
   - TRADE_EXECUTIONS: check for NULLs in compliance_status, track row count, and monitor freshness
   - LISTINGS: check for NULLs in ask_price_per_share and track row count
   - COMPLIANCE_REVIEWS: track row count and monitor freshness
3. Schedule them to trigger on data changes
4. Verify the DMF references are active by querying INFORMATION_SCHEMA.DATA_METRIC_FUNCTION_REFERENCES

Execute everything and show me what's attached."""

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

-- Schedule monitoring
ALTER TABLE TRADE_EXECUTIONS SET DATA_METRIC_SCHEDULE = 'TRIGGER_ON_CHANGES';
```

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
