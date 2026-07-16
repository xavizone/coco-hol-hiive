WITH trades AS (
    SELECT * FROM {{ ref('stg_trades') }}
),

listings AS (
    SELECT * FROM {{ ref('stg_listings') }}
),

companies AS (
    SELECT * FROM {{ source('raw', 'COMPANIES') }}
)

SELECT
    c.company_id,
    c.company_name,
    c.sector,
    c.funding_stage,
    COUNT(DISTINCT t.trade_id) AS total_trades,
    SUM(t.total_value_usd) AS total_trade_volume_usd,
    AVG(t.execution_price_per_share) AS avg_execution_price,
    COUNT(DISTINCT l.listing_id) AS total_listings,
    SUM(CASE WHEN l.is_active THEN 1 ELSE 0 END) AS active_listings,
    CASE
        WHEN SUM(l.shares_offered) > 0
        THEN SUM(t.shares_traded)::FLOAT / SUM(l.shares_offered)
        ELSE 0
    END AS listing_fill_rate
FROM companies c
LEFT JOIN trades t ON t.company_id = c.company_id
LEFT JOIN listings l ON l.company_id = c.company_id
GROUP BY c.company_id, c.company_name, c.sector, c.funding_stage
