# dags/data_pipeline.py
from datetime import datetime
from airflow.sdk import dag, task


@dag(
    start_date=datetime(2026, 1, 1),
    schedule="@daily",
    catchup=False,
    tags=["data-engineering", "nham24"],
)
def nham24_customer_pipeline():

    @task
    def extract():
        from src.extract import extract_customers, save_raw_data

        data = extract_customers()
        print(f"Extracted {len(data)} raw customer records")

        save_raw_data(data, "customers.json")
        return data

    @task
    def transform(raw_data):
        from src.transform import (
            transform_customers,
            transform_addresses,
            transform_payments,
        )

        customers = transform_customers(raw_data)
        addresses = transform_addresses(raw_data)
        payments = transform_payments(raw_data)

        print(f"Transformed {len(customers)} customers")
        print(f"Transformed {len(addresses)} delivery addresses")
        print(f"Transformed {len(payments)} payment methods")

        return {
            "customers": customers,
            "addresses": addresses,
            "payments": payments,
        }

    @task
    def init_schema():
        from src.load import init_db

        init_db()
        print("Database schema verified and ready.")

    @task
    def load_customers_table(transformed_data):
        from src.load import load_customers

        customers = transformed_data["customers"]
        load_customers(customers)
        print(f"Loaded {len(customers)} records into 'customers' table")

    @task
    def load_addresses_table(transformed_data):
        from src.load import load_addresses

        addresses = transformed_data["addresses"]
        load_addresses(addresses)
        print(f"Loaded {len(addresses)} records into 'customer_addresses' table")

    @task
    def load_payments_table(transformed_data):
        from src.load import load_payments

        payments = transformed_data["payments"]
        load_payments(payments)
        print(f"Loaded {len(payments)} records into 'customer_payment_methods' table")

    # Pipeline dependency orchestration
    schema_ready = init_schema()
    raw = extract()
    transformed = transform(raw)

    # Schema must exist before parallel loads start
    schema_ready >> [
        load_customers_table(transformed),
        load_addresses_table(transformed),
        load_payments_table(transformed),
    ]


nham24_customer_pipeline()