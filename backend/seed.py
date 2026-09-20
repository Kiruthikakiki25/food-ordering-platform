"""
seed.py — Seeds branches and a shared menu for the single-brand,
multi-branch Food Ordering & Delivery Platform.

Run once: python seed.py
"""

from app import create_app, db
from app.models import Branch, MenuItem

# ---------------------------------------------------------------------
# Branches — replace with your actual chosen brand's real/plausible
# locations. Keep the city/pincode fields realistic for your area.
# ---------------------------------------------------------------------
BRANCHES = [
    {"name": "Cantonment",     "address": "12 Cantonment Rd",     "city": "Trichy", "pincode": "620001", "phone": "9840000001"},
    {"name": "Thillai Nagar",  "address": "45 Thillai Nagar Main Rd", "city": "Trichy", "pincode": "620018", "phone": "9840000002"},
    {"name": "Srirangam",      "address": "8 Chinthamani St",     "city": "Trichy", "pincode": "620006", "phone": "9840000003"},
    {"name": "K.K. Nagar",     "address": "22 KK Nagar Main Rd",  "city": "Trichy", "pincode": "620021", "phone": "9840000004"},
]

# ---------------------------------------------------------------------
# Menu — one shared menu across every branch. Replace/extend with
# your chosen restaurant's actual (or plausibly reconstructed) menu.
# This is intentionally a smaller, curated list — not 1,200 fabricated
# items — since it's one brand's real menu now, not a marketplace.
# ---------------------------------------------------------------------
MENU_ITEMS = [
    {"name": "Paneer Butter Masala", "category": "Main Course", "price": 220, "veg_flag": True,  "cuisine_tags": "North Indian", "description": "Paneer cubes in a rich tomato-butter gravy."},
    {"name": "Chicken Biryani",      "category": "Main Course", "price": 260, "veg_flag": False, "cuisine_tags": "Biryani",      "description": "Slow-cooked basmati rice with spiced chicken."},
    {"name": "Veg Fried Rice",       "category": "Main Course", "price": 160, "veg_flag": True,  "cuisine_tags": "Chinese",      "description": "Wok-tossed rice with mixed vegetables."},
    {"name": "Masala Dosa",          "category": "Breakfast",   "price": 90,  "veg_flag": True,  "cuisine_tags": "South Indian", "description": "Crisp dosa filled with spiced potato masala."},
    {"name": "Chicken 65",           "category": "Starters",    "price": 190, "veg_flag": False, "cuisine_tags": "South Indian", "description": "Deep-fried spicy chicken bites."},
    {"name": "Gobi Manchurian",      "category": "Starters",    "price": 150, "veg_flag": True,  "cuisine_tags": "Chinese",      "description": "Crispy cauliflower tossed in Indo-Chinese sauce."},
    {"name": "Veg Thali",            "category": "Main Course", "price": 180, "veg_flag": True,  "cuisine_tags": "South Indian", "description": "Full-course meal with rice, sambar, rasam, curries."},
    {"name": "Chicken Kebab",        "category": "Starters",    "price": 210, "veg_flag": False, "cuisine_tags": "North Indian", "description": "Grilled marinated chicken skewers."},
    {"name": "Gulab Jamun",          "category": "Desserts",    "price": 60,  "veg_flag": True,  "cuisine_tags": "Dessert",      "description": "Fried milk dumplings soaked in sugar syrup."},
    {"name": "Filter Coffee",        "category": "Beverages",   "price": 30,  "veg_flag": True,  "cuisine_tags": "South Indian", "description": "Classic South Indian filter coffee."},
]


def seed():
    app = create_app()
    with app.app_context():
        # Branches
        for b in BRANCHES:
            if not Branch.query.filter_by(name=b["name"], city=b["city"]).first():
                db.session.add(Branch(**b))

        # Menu
        for item in MENU_ITEMS:
            if not MenuItem.query.filter_by(name=item["name"]).first():
                db.session.add(MenuItem(**item))

        db.session.commit()
        print(f"Seeded {len(BRANCHES)} branches and {len(MENU_ITEMS)} menu items.")


if __name__ == "__main__":
    seed()