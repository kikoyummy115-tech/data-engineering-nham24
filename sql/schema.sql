-- sql/schema.sql

-- 1. Core Customers Table
CREATE TABLE IF NOT EXISTS customers (
    customer_id TEXT PRIMARY KEY,
    full_name TEXT NOT NULL,
    phone_number TEXT NOT NULL UNIQUE,
    email TEXT,
    is_phone_verified BOOLEAN NOT NULL DEFAULT FALSE,
    preferred_language TEXT NOT NULL DEFAULT 'km',
    preferred_currency TEXT NOT NULL DEFAULT 'USD',
    push_notifications_enabled BOOLEAN NOT NULL DEFAULT TRUE,
    dietary_flags TEXT,
    loyalty_tier TEXT NOT NULL DEFAULT 'Bronze',
    points_balance INTEGER NOT NULL DEFAULT 0,
    lifetime_orders_count INTEGER NOT NULL DEFAULT 0,
    active_coupons_count INTEGER NOT NULL DEFAULT 0,
    registered_channel TEXT NOT NULL,
    last_active_at TIMESTAMP,
    processed_at TIMESTAMP NOT NULL
);

-- 2. Customer Delivery Addresses Table (1:N)
CREATE TABLE IF NOT EXISTS customer_addresses (
    address_id TEXT PRIMARY KEY,
    customer_id TEXT NOT NULL,
    label TEXT NOT NULL,
    is_default BOOLEAN NOT NULL DEFAULT FALSE,
    latitude REAL NOT NULL,
    longitude REAL NOT NULL,
    street TEXT NOT NULL,
    sangkat TEXT NOT NULL,
    khan TEXT NOT NULL,
    city TEXT NOT NULL,
    dropoff_notes TEXT,
    processed_at TIMESTAMP NOT NULL,
    FOREIGN KEY (customer_id) REFERENCES customers (customer_id) ON DELETE CASCADE
);

-- 3. Customer Payment Profiles Table (1:N)
CREATE TABLE IF NOT EXISTS customer_payment_methods (
    payment_method_id TEXT PRIMARY KEY,
    customer_id TEXT NOT NULL,
    payment_type TEXT NOT NULL,
    bank_name TEXT,
    account_mask TEXT,
    is_default BOOLEAN NOT NULL DEFAULT FALSE,
    processed_at TIMESTAMP NOT NULL,
    FOREIGN KEY (customer_id) REFERENCES customers (customer_id) ON DELETE CASCADE
);