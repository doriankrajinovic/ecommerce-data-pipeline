-- Dimension model za customers
-- Dodaje metrike po kupcu

WITH customers AS (
    SELECT * FROM {{ ref('stg_customers') }}
),

orders AS (
    SELECT * FROM {{ ref('stg_orders') }}
),

customer_orders AS (
    SELECT
        customer_id,
        COUNT(*) AS total_orders,
        SUM(total_amount) AS lifetime_value,
        MIN(order_date) AS first_order_date,
        MAX(order_date) AS last_order_date
    FROM orders
    GROUP BY customer_id
)

SELECT
    c.customer_id,
    c.first_name,
    c.last_name,
    c.full_name,
    c.email,
    c.country,
    COALESCE(co.total_orders, 0) AS total_orders,
    COALESCE(co.lifetime_value, 0) AS lifetime_value,
    co.first_order_date,
    co.last_order_date,
    CASE
        WHEN COALESCE(co.lifetime_value, 0) >= 1000 THEN 'Premium'
        WHEN COALESCE(co.lifetime_value, 0) >= 500 THEN 'Regular'
        WHEN COALESCE(co.lifetime_value, 0) > 0 THEN 'Basic'
        ELSE 'New'
    END AS customer_segment

FROM customers c
LEFT JOIN customer_orders co ON c.customer_id = co.customer_id