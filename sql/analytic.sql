
-- Customer Loyalty & Order Velocity by Channel

SELECT 
    registered_channel,
    loyalty_tier,
    COUNT(*) AS total_users,
    ROUND(AVG(lifetime_orders_count), 1) AS avg_orders,
    ROUND(AVG(points_balance), 0) AS avg_points
FROM customers
GROUP BY registered_channel, loyalty_tier
ORDER BY total_users DESC;



-- Top Phnom Penh Delivery Hotspots (Khan & Sangkat)

SELECT 
    a.khan,
    a.sangkat,
    COUNT(a.address_id) AS delivery_points,
    COUNT(DISTINCT a.customer_id) AS unique_customers
FROM customer_addresses a
WHERE a.city = 'Phnom Penh'
GROUP BY a.khan, a.sangkat
ORDER BY delivery_points DESC
LIMIT 10;


-- Payment Method Adoption (Bakong / KHQR vs Cash)

SELECT 
    payment_type,
    COALESCE(bank_name, 'N/A') AS bank_name,
    COUNT(*) AS total_linked,
    SUM(CASE WHEN is_default = 1 THEN 1 ELSE 0 END) AS default_count
FROM customer_payment_methods
GROUP BY payment_type, bank_name
ORDER BY total_linked DESC;