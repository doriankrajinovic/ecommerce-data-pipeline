-- Staging model za products

SELECT
    product_id,
    name AS product_name,
    category,
    CAST(price AS NUMERIC) AS price,
    stock_quantity,
    TIMESTAMP_MICROS(created_at) AS created_at,
    CURRENT_TIMESTAMP() AS loaded_at

FROM {{ source('raw', 'products') }}