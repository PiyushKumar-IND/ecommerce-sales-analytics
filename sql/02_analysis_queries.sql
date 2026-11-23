-- ============================================================
-- E-commerce Sales Analytics: analysis queries (MySQL)
-- Run one query at a time: cursor on the query + Ctrl+Enter
-- ============================================================

USE sql_ecommerce_analytics;

-- ------------------------------------------------------------
-- 1. Data quality checks
-- ------------------------------------------------------------
SELECT * FROM ecommerce_sales_analytics_5000 LIMIT 10;

SELECT COUNT(*) AS total_records FROM ecommerce_sales_analytics_5000;

-- Rows with missing values (expected: 0)
SELECT COUNT(*) AS rows_with_nulls
FROM ecommerce_sales_analytics_5000
WHERE order_id IS NULL OR customer_id IS NULL OR revenue IS NULL
   OR customer_rating IS NULL OR region IS NULL OR product_category IS NULL;

-- Duplicate order IDs (expected: 0 rows)
SELECT order_id, COUNT(*) AS times_seen
FROM ecommerce_sales_analytics_5000
GROUP BY order_id
HAVING COUNT(*) > 1;

-- ------------------------------------------------------------
-- 2. Key performance indicators (KPIs)
-- ------------------------------------------------------------
SELECT
    ROUND(SUM(revenue), 2)         AS total_revenue,
    COUNT(DISTINCT order_id)       AS total_orders,
    COUNT(DISTINCT customer_id)    AS total_customers,
    SUM(quantity)                  AS total_products_sold,
    ROUND(AVG(revenue), 2)         AS avg_order_value,
    ROUND(AVG(customer_rating), 2) AS avg_rating
FROM ecommerce_sales_analytics_5000;

-- ------------------------------------------------------------
-- 3. Revenue by region
-- ------------------------------------------------------------
SELECT region, ROUND(SUM(revenue), 2) AS total_revenue
FROM ecommerce_sales_analytics_5000
GROUP BY region
ORDER BY total_revenue DESC;

-- ------------------------------------------------------------
-- 4. Orders by payment method
-- ------------------------------------------------------------
SELECT payment_method, COUNT(*) AS num_orders
FROM ecommerce_sales_analytics_5000
GROUP BY payment_method
ORDER BY num_orders DESC;

-- ------------------------------------------------------------
-- 5. Monthly revenue
-- ------------------------------------------------------------
-- By calendar month (all years combined)
SELECT month, ROUND(SUM(revenue), 2) AS monthly_revenue
FROM ecommerce_sales_analytics_5000
GROUP BY month
ORDER BY month;

-- By year and month
SELECT `year_month`, ROUND(SUM(revenue), 2) AS monthly_revenue
FROM ecommerce_sales_analytics_5000
GROUP BY `year_month`
ORDER BY `year_month`;

-- ------------------------------------------------------------
-- 6. Product category analysis
-- ------------------------------------------------------------
SELECT product_category, ROUND(AVG(customer_rating), 2) AS avg_rating
FROM ecommerce_sales_analytics_5000
GROUP BY product_category
ORDER BY avg_rating DESC;

SELECT
    product_category,
    ROUND(SUM(revenue), 2) AS total_revenue,
    ROUND(AVG(revenue), 2) AS avg_revenue,
    MAX(revenue)           AS max_revenue,
    MIN(revenue)           AS min_revenue,
    COUNT(*)               AS num_orders
FROM ecommerce_sales_analytics_5000
GROUP BY product_category
ORDER BY total_revenue DESC;

-- ------------------------------------------------------------
-- 7. Top 10 customers by spending
-- ------------------------------------------------------------
SELECT customer_id,
       COUNT(*)               AS orders,
       ROUND(SUM(revenue), 2) AS total_spent
FROM ecommerce_sales_analytics_5000
GROUP BY customer_id
ORDER BY total_spent DESC
LIMIT 10;

-- ------------------------------------------------------------
-- 8. Discount impact on revenue and ratings
-- ------------------------------------------------------------
SELECT
    CASE
        WHEN discount < 0.10 THEN 'Low (under 10%)'
        WHEN discount < 0.20 THEN 'Medium (10-20%)'
        ELSE 'High (20%+)'
    END AS discount_level,
    COUNT(*)                        AS orders,
    ROUND(AVG(revenue), 2)          AS avg_revenue,
    ROUND(AVG(customer_rating), 2)  AS avg_rating
FROM ecommerce_sales_analytics_5000
GROUP BY discount_level
ORDER BY discount_level;

-- ------------------------------------------------------------
-- 9. Delivery performance by region
-- ------------------------------------------------------------
SELECT region,
       ROUND(AVG(delivery_days), 1)   AS avg_delivery_days,
       ROUND(AVG(customer_rating), 2) AS avg_rating
FROM ecommerce_sales_analytics_5000
GROUP BY region
ORDER BY avg_delivery_days;
