-- Fact model za dnevni revenue
-- Agregira prodaju po danu

WITH orders AS (
    SELECT * FROM {{ ref('stg_orders') }}
)

SELECT
    order_date_day AS date,
    order_year,
    order_month,
    COUNT(*) AS total_orders,
    SUM(total_amount) AS total_revenue,
    AVG(total_amount) AS avg_order_value,
    COUNT(CASE WHEN status = 'delivered' THEN 1 END) AS delivered_orders,
    COUNT(CASE WHEN status = 'cancelled' THEN 1 END) AS cancelled_orders,
    COUNT(CASE WHEN status = 'pending' THEN 1 END) AS pending_orders

FROM orders
GROUP BY order_date_day, order_year, order_month
ORDER BY date
