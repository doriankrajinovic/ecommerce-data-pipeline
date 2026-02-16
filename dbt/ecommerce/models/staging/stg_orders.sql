-- Staging model za orders
-- TIMESTAMP_MICROS konvertira INT64 (Unix mikrosekunde) u TIMESTAMP

SELECT 
    order_id, 
    customer_id, 
    TIMESTAMP_MICROS(CAST(order_date / 1000 AS INT64)) AS order_date,
    status, 
    CAST(total_amount AS NUMERIC) AS total_amount, 
    DATE(TIMESTAMP_MICROS(CAST(order_date / 1000 AS INT64))) AS order_date_day, 
    EXTRACT(YEAR FROM TIMESTAMP_MICROS(CAST(order_date / 1000 AS INT64))) AS order_year, 
    EXTRACT(MONTH FROM TIMESTAMP_MICROS(CAST(order_date / 1000 AS INT64))) AS order_month, 
    CURRENT_TIMESTAMP() AS loaded_at

FROM {{ source('raw', 'orders') }}