from extract import extract_customers, save_raw_data
from transform import (
    transform_customers,
    transform_addresses,
    transform_payments,
)
from load import (
    init_db,
    load_customers,
    load_addresses,
    load_payments,
)


def run_pipeline():
    print("0. Initializing database schema...")
    init_db()

    print("1. Extracting data...")
    raw_customers = extract_customers()
    print(f"Extracted {len(raw_customers)} raw customer records")

    raw_file = save_raw_data(raw_customers, "customers.json")
    print(f"Saved raw landing payload to {raw_file}")

    print("2. Transforming data...")
    clean_customers = transform_customers(raw_customers)
    clean_addresses = transform_addresses(raw_customers)
    clean_payments = transform_payments(raw_customers)

    print(f"Transformed {len(clean_customers)} customers")
    print(f"Transformed {len(clean_addresses)} addresses")
    print(f"Transformed {len(clean_payments)} payment methods")

    print("3. Loading into database...")
    load_customers(clean_customers)
    load_addresses(clean_addresses)
    load_payments(clean_payments)

    print("Pipeline completed successfully. Ready for analytics!")


if __name__ == "__main__":
    run_pipeline()