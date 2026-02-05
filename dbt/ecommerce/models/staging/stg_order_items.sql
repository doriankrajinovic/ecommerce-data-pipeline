-- Staging model za order_items

SELECT
    order_item_id,
    order_id,
    product_id,
    quantity,
    CAST(unit_price AS NUMERIC) AS unit_price,
    CAST(quantity * unit_price AS NUMERIC) AS line_total,
    CURRENT_TIMESTAMP() AS loaded_at

FROM {{ source('raw', 'order_items') }}
