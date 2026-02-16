-- Staging model za products

SELECT
    product_id,
    name AS product_name,
    category,
    CAST(price AS NUMERIC) AS price,
    stock_quantity,
    TIMESTAMP_MICROS(CAST(created_at / 1000 AS INT64)) AS created_at,
    CURRENT_TIMESTAMP() AS loaded_at

FROM {{ source('raw', 'products') }}