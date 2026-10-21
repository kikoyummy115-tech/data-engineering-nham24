import unittest

from datetime import datetime


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
        "processed_at": datetime.utcnow(),
    }

class TestCustomerTransformation(unittest.TestCase):

    def setUp(self):
        # Sample raw record with edge cases: spaces, uppercase email/currency
        self.raw_customer = {
            "customer_id": "c7f21b84-482a-4a7b-a25c-8973b06e931d",
            "identity": {
                "phone": " +85512999888 ",
                "name": "  Sophea Chan  ",
                "email": "Sophea.Chan@EXAMPLE.com",
                "is_phone_verified": True,
                "avatar_url": "https://cdn.nham24.com/avatars/c7f21b84.webp"
            },
            "preferences": {
                "language": " KM ",
                "currency": "usd",
                "push_notifications_enabled": 1,
                "dietary_flags": ["halal_only", "vegetarian"]
            },
            "loyalty": {
                "tier": "silver",
                "points_balance": "1450",
                "lifetime_orders_count": "86",
                "active_coupons": [{"code": "NHAMFREESHIP"}]
            },
            "metadata": {
                "registered_channel": " IOS_APP ",
                "last_active_at": "2026-10-21T02:40:00Z"
            }
        }

    def test_transform_customer_fields_and_types(self):
        result = transform_customer(self.raw_customer)

        # 1. Identity & Normalization
        self.assertEqual(result["customer_id"], "c7f21b84-482a-4a7b-a25c-8973b06e931d")
        self.assertEqual(result["full_name"], "Sophea Chan")
        self.assertEqual(result["phone_number"], "+85512999888")
        self.assertEqual(result["email"], "sophea.chan@example.com")
        self.assertIs(result["is_phone_verified"], True)

        # 2. Preferences & Parsing
        self.assertEqual(result["preferred_language"], "km")
        self.assertEqual(result["preferred_currency"], "USD")
        self.assertIs(result["push_notifications_enabled"], True)
        self.assertEqual(result["dietary_flags"], "halal_only;vegetarian")

        # 3. Numeric conversions & Counts
        self.assertEqual(result["loyalty_tier"], "Silver")
        self.assertEqual(result["points_balance"], 1450)
        self.assertIsInstance(result["points_balance"], int)
        self.assertEqual(result["lifetime_orders_count"], 86)
        self.assertEqual(result["active_coupons_count"], 1)

        # 4. Metadata & Audit tracking
        self.assertEqual(result["registered_channel"], "ios_app")
        self.assertEqual(result["last_active_at"], "2026-10-21T02:40:00Z")
        self.assertIsInstance(result["processed_at"], datetime)


if __name__ == "__main__":
    unittest.main()