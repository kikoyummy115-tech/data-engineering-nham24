# src/load.py
import os
from pathlib import Path
import psycopg

DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql://postgres:na123@localhost:5432/datawarehouse"
)
SCHEMA_PATH = Path("sql/schema.sql")


def init_db():
    with psycopg.connect(DATABASE_URL) as connection:
        with connection.cursor() as cursor:
            with open(SCHEMA_PATH, "r", encoding="utf-8") as schema_file:
                cursor.execute(schema_file.read())
        connection.commit()


def load_customers(customers):
    with psycopg.connect(DATABASE_URL) as connection:
        with connection.cursor() as cursor:
            for customer in customers:
                cursor.execute(
                    """
                    INSERT INTO customers (
                        customer_id,
                        full_name,
                        phone_number,
                        email,
                        is_phone_verified,
                        preferred_language,
                        preferred_currency,
                        push_notifications_enabled,
                        dietary_flags,
                        loyalty_tier,
                        points_balance,
                        lifetime_orders_count,
                        active_coupons_count,
                        registered_channel,
                        last_active_at,
                        processed_at
                    )
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                    ON CONFLICT (customer_id)
                    DO UPDATE SET
                        full_name = EXCLUDED.full_name,
                        phone_number = EXCLUDED.phone_number,
                        email = EXCLUDED.email,
                        is_phone_verified = EXCLUDED.is_phone_verified,
                        preferred_language = EXCLUDED.preferred_language,
                        preferred_currency = EXCLUDED.preferred_currency,
                        push_notifications_enabled = EXCLUDED.push_notifications_enabled,
                        dietary_flags = EXCLUDED.dietary_flags,
                        loyalty_tier = EXCLUDED.loyalty_tier,
                        points_balance = EXCLUDED.points_balance,
                        lifetime_orders_count = EXCLUDED.lifetime_orders_count,
                        active_coupons_count = EXCLUDED.active_coupons_count,
                        registered_channel = EXCLUDED.registered_channel,
                        last_active_at = EXCLUDED.last_active_at,
                        processed_at = EXCLUDED.processed_at
                    """,
                    (
                        customer["customer_id"],
                        customer["full_name"],
                        customer["phone_number"],
                        customer["email"],
                        customer["is_phone_verified"],
                        customer["preferred_language"],
                        customer["preferred_currency"],
                        customer["push_notifications_enabled"],
                        customer["dietary_flags"],
                        customer["loyalty_tier"],
                        customer["points_balance"],
                        customer["lifetime_orders_count"],
                        customer["active_coupons_count"],
                        customer["registered_channel"],
                        customer["last_active_at"],
                        customer["processed_at"],
                    ),
                )
        connection.commit()


def load_addresses(addresses):
    with psycopg.connect(DATABASE_URL) as connection:
        with connection.cursor() as cursor:
            for addr in addresses:
                cursor.execute(
                    """
                    INSERT INTO customer_addresses (
                        address_id,
                        customer_id,
                        label,
                        is_default,
                        latitude,
                        longitude,
                        street,
                        sangkat,
                        khan,
                        city,
                        dropoff_notes,
                        processed_at
                    )
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                    ON CONFLICT (address_id)
                    DO UPDATE SET
                        customer_id = EXCLUDED.customer_id,
                        label = EXCLUDED.label,
                        is_default = EXCLUDED.is_default,
                        latitude = EXCLUDED.latitude,
                        longitude = EXCLUDED.longitude,
                        street = EXCLUDED.street,
                        sangkat = EXCLUDED.sangkat,
                        khan = EXCLUDED.khan,
                        city = EXCLUDED.city,
                        dropoff_notes = EXCLUDED.dropoff_notes,
                        processed_at = EXCLUDED.processed_at
                    """,
                    (
                        addr["address_id"],
                        addr["customer_id"],
                        addr["label"],
                        addr["is_default"],
                        addr["latitude"],
                        addr["longitude"],
                        addr["street"],
                        addr["sangkat"],
                        addr["khan"],
                        addr["city"],
                        addr["dropoff_notes"],
                        addr["processed_at"],
                    ),
                )
        connection.commit()


def load_payments(payments):
    with psycopg.connect(DATABASE_URL) as connection:
        with connection.cursor() as cursor:
            for pay in payments:
                cursor.execute(
                    """
                    INSERT INTO customer_payment_methods (
                        payment_method_id,
                        customer_id,
                        payment_type,
                        bank_name,
                        account_mask,
                        is_default,
                        processed_at
                    )
                    VALUES (%s, %s, %s, %s, %s, %s, %s)
                    ON CONFLICT (payment_method_id)
                    DO UPDATE SET
                        customer_id = EXCLUDED.customer_id,
                        payment_type = EXCLUDED.payment_type,
                        bank_name = EXCLUDED.bank_name,
                        account_mask = EXCLUDED.account_mask,
                        is_default = EXCLUDED.is_default,
                        processed_at = EXCLUDED.processed_at
                    """,
                    (
                        pay["payment_method_id"],
                        pay["customer_id"],
                        pay["payment_type"],
                        pay["bank_name"],
                        pay["account_mask"],
                        pay["is_default"],
                        pay["processed_at"],
                    ),
                )
        connection.commit()