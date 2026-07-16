WITH source AS (
    SELECT * FROM {{ source('raw', 'TRADE_EXECUTIONS') }}
)

SELECT
    trade_id,
    listing_id,
    company_id,
    trade_date,
    trade_type,
    shares_traded,
    execution_price_per_share,
    total_value_usd,
    commission_pct,
    compliance_status,
    settlement_date
FROM source
WHERE trade_id IS NOT NULL
