-- Staging model za customers 
-- Cisti i standardizira podatke o kupcima 

SELECT
    customer_id,
    first_name,
    last_name,
    CONCAT(first_name, ' ', last_name) AS full_name,
    LOWER(email) AS email,
    country,
    TIMESTAMP_MICROS(CAST(created_at / 1000 AS INT64)) AS created_at,
    CURRENT_TIMESTAMP() AS loaded_at
FROM {{ source('raw', 'customers') }}