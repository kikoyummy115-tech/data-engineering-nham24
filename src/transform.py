from datetime import datetime, timezone


# --- 1. Single-Record Transformers ---

def transform_customer(customer):
    identity = customer["identity"]
    prefs = customer["preferences"]
    loyalty = customer["loyalty"]
    meta = customer["metadata"]

    return {
        "customer_id": str(customer["customer_id"]),
        "full_name": identity["name"].strip(),
        "phone_number": identity["phone"].strip(),
        "email": identity["email"].strip().lower(),
        "is_phone_verified": bool(identity["is_phone_verified"]),
        "preferred_language": prefs["language"].strip().lower(),
        "preferred_currency": prefs["currency"].strip().upper(),
        "push_notifications_enabled": bool(prefs["push_notifications_enabled"]),
        "dietary_flags": ";".join(prefs["dietary_flags"]),
        "loyalty_tier": loyalty["tier"].strip().title(),
        "points_balance": int(loyalty["points_balance"]),
        "lifetime_orders_count": int(loyalty["lifetime_orders_count"]),
        "active_coupons_count": len(loyalty["active_coupons"]),
        "registered_channel": meta["registered_channel"].strip().lower(),
        "last_active_at": meta["last_active_at"],
        "processed_at": datetime.now(timezone.utc),
    }


def transform_customer_address(customer_id, address):
    coords = address["coordinates"]
    return {
        "address_id": str(address["address_id"]),
        "customer_id": str(customer_id),
        "label": address["label"].strip().title(),
        "is_default": bool(address["is_default"]),
        "latitude": float(coords["latitude"]),
        "longitude": float(coords["longitude"]),
        "street": address["street"].strip(),
        "sangkat": address["sangkat"].strip(),
        "khan": address["khan"].strip(),
        "city": address["city"].strip(),
        "dropoff_notes": address["dropoff_notes"].strip() if address.get("dropoff_notes") else None,
        "processed_at": datetime.now(timezone.utc),
    }


def transform_customer_payment(customer_id, payment):
    return {
        "payment_method_id": str(payment["method_id"]),
        "customer_id": str(customer_id),
        "payment_type": payment["type"].strip().upper(),
        "bank_name": payment.get("bank_name"),
        "account_mask": payment.get("account_mask"),
        "is_default": bool(payment["is_default"]),
        "processed_at": datetime.now(timezone.utc),
    }


# --- 2. Batch List Comprehension Transformers ---

def transform_customers(customers):
    return [
        transform_customer(customer)
        for customer in customers
    ]


def transform_addresses(customers):
    return [
        transform_customer_address(customer["customer_id"], address)
        for customer in customers
        for address in customer["addresses"]
    ]


def transform_payments(customers):
    return [
        transform_customer_payment(customer["customer_id"], payment)
        for customer in customers
        for payment in customer["payment_profiles"]
    ]