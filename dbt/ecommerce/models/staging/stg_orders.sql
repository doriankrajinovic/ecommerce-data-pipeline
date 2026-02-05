-- Staging model za orders
-- TIMESTAMP_MICROS konvertira INT64 (Unix mikrosekunde) u TIMESTAMP

SELECT 
    order_id, 
    customer_id, 
    TIMESTAMP_MICROS(order_date) AS order_date,
    status, 
    CAST(total_amount AS NUMERIC) AS total_amount, 
    DATE(TIMESTAMP_MICROS(order_date)) AS order_date_day, 
    EXTRACT(YEAR FROM TIMESTAMP_MICROS(order_date)) AS order_year, 
    EXTRACT(MONTH FROM TIMESTAMP_MICROS(order_date)) AS order_month, 
    CURRENT_TIMESTAMP() AS loaded_at

FROM {{ source('raw', 'orders') }}