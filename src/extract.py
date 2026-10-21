import json
from pathlib import Path
import requests

# Standard RESTful collection endpoint for batch customer profiles
CUSTOMERS_API_URL = "http://localhost:5000/api/v1/customers"

RAW_DIR = Path("data/raw")


def extract_customers():
    # Pass params if your mock Flask/FastAPI server supports pagination limits
    response = requests.get(CUSTOMERS_API_URL, timeout=30)
    response.raise_for_status()
    return response.json()


def save_raw_data(data, filename: str):
    RAW_DIR.mkdir(parents=True, exist_ok=True)
    output_file = RAW_DIR / filename

    with output_file.open("w", encoding="utf-8") as file:
        json.dump(data, file, indent=2, ensure_ascii=False)

    return output_file


def main():

    # 2. Extract and save Nham24 customer records
    try:
        customers_data = extract_customers()
        customers_file = save_raw_data(customers_data, "customers.json")
        print(f"Saved {len(customers_data)} customer records to {customers_file}")
    except requests.exceptions.ConnectionError:
        print(f"Failed to connect to {CUSTOMERS_API_URL}. Is your local server running on port 5000?")


if __name__ == "__main__":
    main()