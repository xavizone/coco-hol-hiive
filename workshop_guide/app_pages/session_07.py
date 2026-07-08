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


PROMPT_7_1 = """In your workshop schema in HIIVE_COCO_HOL, set up Data Metric Functions (DMFs) for continuous monitoring of our critical tables.

1. Set up the event table for DMF results:
ALTER DATABASE HIIVE_COCO_HOL SET DATA_METRIC_SCHEDULE_EVENT_TABLE = 'HIIVE_COCO_HOL.' || CURRENT_USER() || '_OPS.DMF_EVENTS';

2. Apply built-in system DMFs to our critical tables:
   - TRADE_EXECUTIONS: NULL_COUNT on compliance_status, ROW_COUNT, FRESHNESS
   - LISTINGS: NULL_COUNT on ask_price_per_share, ROW_COUNT
   - COMPLIANCE_REVIEWS: ROW_COUNT, FRESHNESS

3. Schedule them to run on changes:
ALTER TABLE TRADE_EXECUTIONS SET DATA_METRIC_SCHEDULE = 'TRIGGER_ON_CHANGES';

4. Verify the DMF references are active:
SELECT * FROM TABLE(INFORMATION_SCHEMA.DATA_METRIC_FUNCTION_REFERENCES(
  REF_ENTITY_NAME => '<your schema>.TRADE_EXECUTIONS',
  REF_ENTITY_DOMAIN => 'TABLE'
));

Execute all SQL and confirm DMFs are attached."""

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


PROMPT_7_2 = """In your workshop schema in HIIVE_COCO_HOL, create custom Data Metric Functions for anomaly detection specific to our marketplace operations.

1. Create a trade volume anomaly DMF (flags if today's volume is >2 standard deviations from the 30-day rolling average):

CREATE OR REPLACE DATA METRIC FUNCTION trade_volume_anomaly_check(
  ARG_T TABLE(total_value_usd NUMBER, trade_date DATE)
)
RETURNS NUMBER
AS
$$
  SELECT CASE 
    WHEN today_volume > avg_volume + (2 * stddev_volume) THEN 1
    WHEN today_volume < avg_volume - (2 * stddev_volume) THEN -1
    ELSE 0
  END
  FROM (
    SELECT 
      SUM(CASE WHEN trade_date = CURRENT_DATE() THEN total_value_usd ELSE 0 END) as today_volume,
      AVG(CASE WHEN trade_date < CURRENT_DATE() THEN total_value_usd END) as avg_volume,
      STDDEV(CASE WHEN trade_date < CURRENT_DATE() THEN total_value_usd END) as stddev_volume
    FROM ARG_T
    WHERE trade_date >= DATEADD(day, -30, CURRENT_DATE())
  )
$$;

2. Create a pricing deviation DMF (flags trades >20% below latest 409A valuation):

CREATE OR REPLACE DATA METRIC FUNCTION pricing_deviation_check(
  ARG_T TABLE(execution_price_per_share NUMBER, company_id VARCHAR)
)
RETURNS NUMBER
AS
$$
  SELECT COUNT(*)
  FROM ARG_T t
  JOIN PRICING_SIGNALS p ON t.company_id = p.company_id
  WHERE p.signal_type = '409a_valuation'
    AND p.signal_date = (SELECT MAX(signal_date) FROM PRICING_SIGNALS WHERE company_id = t.company_id AND signal_type = '409a_valuation')
    AND t.execution_price_per_share < p.price_per_share * 0.8
$$;

3. Create a compliance backlog DMF (flags if unresolved reviews exceed threshold):

CREATE OR REPLACE DATA METRIC FUNCTION compliance_backlog_check(
  ARG_T TABLE(outcome VARCHAR, review_date DATE)
)
RETURNS NUMBER
AS
$$
  SELECT COUNT(*)
  FROM ARG_T
  WHERE outcome IN ('escalated', 'conditionally_approved')
    AND review_date < DATEADD(day, -7, CURRENT_DATE())
$$;

4. Apply these custom DMFs to the appropriate tables and verify.

Execute all SQL."""

render_prompt("Prompt 7.2", "Create Custom DMFs for Anomaly Detection", PROMPT_7_2)

render_explanation("What this prompt does", """
Creates business-specific anomaly detection that goes far beyond generic null checks:

- **trade_volume_anomaly_check**: Statistical anomaly detection using rolling 30-day window. Returns 1 (spike), -1 (drop), or 0 (normal).
- **pricing_deviation_check**: Cross-references trade prices against 409A valuations. Flags regulatory risk.
- **compliance_backlog_check**: Monitors review aging. Catches operational bottlenecks before they become compliance issues.

**Why this matters for HIIVE**: Your current dbt Elementary setup only runs when dbt runs (GitHub Actions). These DMFs run continuously on Snowflake's schedule — catching issues BETWEEN dbt runs.
""")


PROMPT_7_3 = """In your workshop schema in HIIVE_COCO_HOL, set up alerting on DMF results so anomalies trigger notifications automatically.

1. Query recent DMF results from the event table:
SELECT 
  METRIC_NAME,
  TABLE_NAME, 
  VALUE,
  MEASUREMENT_TIME,
  TABLE_SCHEMA
FROM DMF_EVENTS
ORDER BY MEASUREMENT_TIME DESC
LIMIT 20;

2. Create an alert that fires when trade volume anomaly is detected:

CREATE OR REPLACE ALERT trade_volume_alert
  WAREHOUSE = HIIVE_COCO_HOL_WH
  SCHEDULE = 'USING CRON 0 * * * * America/Vancouver'
  IF (EXISTS (
    SELECT 1 FROM DMF_EVENTS
    WHERE METRIC_NAME = 'TRADE_VOLUME_ANOMALY_CHECK'
      AND VALUE != 0
      AND MEASUREMENT_TIME > DATEADD(hour, -1, CURRENT_TIMESTAMP())
  ))
  THEN
    CALL SYSTEM$SEND_EMAIL(
      'hiive_alerts',
      'data-team@hiive.com',
      'ALERT: Trade Volume Anomaly Detected',
      'A trade volume anomaly was detected. Please investigate in the DMF_EVENTS table.'
    );

3. Resume the alert:
ALTER ALERT trade_volume_alert RESUME;

4. Show how to query historical DMF trends:
SELECT 
  METRIC_NAME,
  TABLE_NAME,
  VALUE,
  DATE_TRUNC('hour', MEASUREMENT_TIME) as hour,
  COUNT(*) as measurements
FROM DMF_EVENTS
GROUP BY 1, 2, 3, 4
ORDER BY hour DESC;

Execute all SQL and explain how this compares to the current dbt Elementary setup."""

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
