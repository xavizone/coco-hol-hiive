WITH source AS (
    SELECT * FROM {{ source('raw', 'LISTINGS') }}
)

SELECT
    listing_id,
    company_id,
    shareholder_id,
    listing_type,
    status,
    shares_offered,
    ask_price_per_share,
    listed_date,
    CASE WHEN status = 'active' THEN TRUE ELSE FALSE END AS is_active
FROM source
WHERE listing_id IS NOT NULL
