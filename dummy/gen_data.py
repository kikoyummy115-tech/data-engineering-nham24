import json
import random
import uuid
from datetime import datetime, timedelta

first_names = [
    "Sophea", "Borey", "Chann", "Dara", "Kosal", "Vannak", "Sokha", "Piseth",
    "Thyda", "Rithy", "Chenda", "Samnang", "Bopha", "Sreypov", "Kolab", "Veasna",
    "Phalla", "Makara", "Chhaya", "Sothea", "Vireak", "Monita", "Neary", "Kiri"
]
last_names = [
    "Chan", "Sok", "Chea", "Kim", "Lim", "Heng", "Keo", "Meas",
    "Pich", "Ros", "Mao", "Ouk", "Tep", "Ung", "Khun", "Chhorn"
]
expat_names = ["Liam Smith", "Chloe Martin", "Marc Dupont", "Emma Davis", "David Miller"]

districts_pp = [
    ("Boeung Keng Kang", "Boeung Keng Kang 1", 11.5512, 104.9254),
    ("Boeung Keng Kang", "Boeung Keng Kang 2", 11.5471, 104.9190),
    ("Boeung Keng Kang", "Toul Svay Prey 1", 11.5435, 104.9088),
    ("Daun Penh", "Wat Phnom", 11.5732, 104.9211),
    ("Daun Penh", "Phsar Thmey 1", 11.5691, 104.9225),
    ("Chamkarmon", "Tonle Bassac", 11.5489, 104.9345),
    ("Toul Kork", "Boeung Kak 1", 11.5765, 104.8992),
    ("Mean Chey", "Chak Angre Kraom", 11.5245, 104.9215),
    ("Chroy Changvar", "Chroy Changvar", 11.5912, 104.9385),
    ("Sen Sok", "Phnom Penh Thmey", 11.5780, 104.8690)
]

districts_sr = [
    ("Siem Reap Municipality", "Svay Dangkum", 13.3533, 103.8554),
    ("Siem Reap Municipality", "Sala Kamreuk", 13.3490, 103.8642)
]

banks = ["ABA Bank", "ACLEDA Bank", "Wing Bank", "Canadia Bank", "Sathapana Bank"]
tiers = [("Bronze", 0, 20), ("Silver", 21, 100), ("Gold", 101, 300), ("Platinum", 301, 1000)]
coupons = ["NHAMFREESHIP", "LUNCH15", "DISCOUNT2USD", "WEEKENDTREAT", "WELCOME2026"]
phone_prefixes = ["+85512", "+85517", "+85570", "+85586", "+85598", "+85596", "+85561"]

records = []
now = datetime(2026, 10, 21, 9, 0, 0)

for i in range(1, 101):
    c_id = str(uuid.uuid4())
    is_expat = random.random() < 0.15
    name = random.choice(expat_names) if is_expat else f"{random.choice(first_names)} {random.choice(last_names)}"
    slug = name.lower().replace(" ", ".")
    phone = f"{random.choice(phone_prefixes)}{random.randint(100000, 999999)}"
    
    tier_info = random.choices(tiers, weights=[0.45, 0.35, 0.15, 0.05])[0]
    tier_name = tier_info[0]
    lifetime_orders = random.randint(tier_info[1], tier_info[2])
    points = lifetime_orders * random.randint(15, 25)
    
    # Generate 1 or 2 addresses
    addr_list = []
    num_addr = 2 if random.random() < 0.35 else 1
    for a_idx in range(num_addr):
        loc = random.choice(districts_sr) if random.random() < 0.1 else random.choice(districts_pp)
        city = "Siem Reap" if "Siem Reap" in loc[0] else "Phnom Penh"
        addr_list.append({
            "address_id": f"addr_{i:04d}_{a_idx+1}",
            "label": "Home" if a_idx == 0 else "Office",
            "is_default": (a_idx == 0),
            "coordinates": {
                "latitude": round(loc[2] + random.uniform(-0.005, 0.005), 7),
                "longitude": round(loc[3] + random.uniform(-0.005, 0.005), 7)
            },
            "street": f"Street {random.choice([51, 63, 178, 271, 310, 2004])}, Building {random.randint(1, 150)}",
            "sangkat": loc[1],
            "khan": loc[0],
            "city": city,
            "dropoff_notes": random.choice([
                "Call upon arrival", "Leave with security guard", "Deliver to door floor 3", "Leave at gate"
            ])
        })

    # Payment profiles
    pay_methods = [
        {
            "method_id": f"pay_{i:04d}_1",
            "type": "KHQR_DIRECT",
            "bank_name": random.choice(banks),
            "account_mask": f"••••{random.randint(1000, 9999)}",
            "is_default": True
        }
    ]
    if random.random() < 0.5:
        pay_methods.append({
            "method_id": f"pay_{i:04d}_2",
            "type": "CASH_ON_DELIVERY",
            "accepted_currencies": ["USD", "KHR"],
            "is_default": False
        })

    user_coupons = []
    if random.random() < 0.4:
        user_coupons.append({
            "code": random.choice(coupons),
            "discount_type": "free_delivery" if "SHIP" in coupons else "amount_discount",
            "valid_until": "2026-12-31T23:59:59Z"
        })

    last_active = now - timedelta(days=random.randint(0, 45), minutes=random.randint(0, 1440))

    record = {
        "customer_id": c_id,
        "identity": {
            "phone": phone,
            "name": name,
            "email": f"{slug}_{random.randint(10, 99)}@example.com",
            "is_phone_verified": random.random() < 0.95,
            "avatar_url": f"https://cdn.nham24.com/avatars/{c_id[:8]}.webp"
        },
        "preferences": {
            "language": "en" if is_expat else random.choice(["km", "km", "en"]),
            "currency": "USD" if (is_expat or random.random() < 0.8) else "KHR",
            "push_notifications_enabled": random.random() < 0.85,
            "dietary_flags": random.sample(["halal_only", "vegetarian", "no_pork", "spicy_level_zero"], k=random.randint(0, 2))
        },
        "addresses": addr_list,
        "payment_profiles": pay_methods,
        "loyalty": {
            "tier": tier_name,
            "points_balance": points,
            "lifetime_orders_count": lifetime_orders,
            "active_coupons": user_coupons
        },
        "metadata": {
            "registered_channel": random.choice(["ios_app", "android_app", "huawei_app_gallery"]),
            "last_active_at": last_active.isoformat() + "Z"
        }
    }
    records.append(record)

# Save to disk
with open("customers_100.json", "w", encoding="utf-8") as f:
    json.dump(records, f, indent=2, ensure_ascii=False)

print(f"Successfully generated {len(records)} realistic Nham24 customer records into customers_100.json.")