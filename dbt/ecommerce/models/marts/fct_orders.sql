-- Fact model za orders
-- Obogaćuje narudžbe s dodatnim podacima

WITH orders AS (
    SELECT * FROM {{ ref('stg_orders') }}
),

order_items AS (
    SELECT * FROM {{ ref('stg_order_items') }}
),

customers AS (
    SELECT * FROM {{ ref('stg_customers') }}
),

order_item_summary AS (
    SELECT
        order_id,
        COUNT(*) AS num_items,
        SUM(quantity) AS total_quantity
    FROM order_items
    GROUP BY order_id
)

SELECT
    o.order_id,
    o.customer_id,
    c.full_name AS customer_name,
    c.country AS customer_country,
    o.order_date,
    o.status,
    o.total_amount,
    COALESCE(ois.num_items, 0) AS num_items,
    COALESCE(ois.total_quantity, 0) AS total_quantity

FROM orders o
LEFT JOIN customers c ON o.customer_id = c.customer_id
LEFT JOIN order_item_summary ois ON o.order_id = ois.order_id
