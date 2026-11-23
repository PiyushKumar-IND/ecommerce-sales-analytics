-- ============================================================
-- E-commerce Sales Analytics: database and table setup (MySQL)
-- Run this ONCE, then import data/ecommerce_cleaned.csv with
-- MySQL Workbench > right-click table > Table Data Import Wizard
-- (choose "Use existing table").
-- ============================================================

CREATE DATABASE IF NOT EXISTS sql_ecommerce_analytics;
USE sql_ecommerce_analytics;

CREATE TABLE IF NOT EXISTS ecommerce_sales_analytics_5000 (
    order_id         INT,
    order_date       DATE,
    customer_id      INT,
    product_category VARCHAR(50),
    region           VARCHAR(50),
    quantity         INT,
    unit_price       DECIMAL(10,2),
    discount         DECIMAL(4,2),
    payment_method   VARCHAR(50),
    delivery_days    INT,
    customer_rating  DECIMAL(3,1),
    revenue          DECIMAL(12,2),
    month            INT,
    year             INT,
    `year_month`     VARCHAR(7)   -- backticks needed: YEAR_MONTH is a reserved word in MySQL
);

-- Check the import worked (expected: 5000)
SELECT COUNT(*) AS total_records FROM ecommerce_sales_analytics_5000;
