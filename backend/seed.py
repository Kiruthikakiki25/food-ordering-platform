# backend/seed.py
import random
import pandas as pd
from app import create_app, db
from app.models import Restaurant, MenuItem

CSV_PATH = "data/zomato.csv"

# Cuisine -> sample dish name pools, since Zomato dataset has no item-level data
DISH_POOL = {
    "Chinese": ["Veg Manchurian", "Chicken Fried Rice", "Hakka Noodles", "Chilli Paneer"],
    "North Indian": ["Butter Chicken", "Paneer Butter Masala", "Dal Makhani", "Garlic Naan"],
    "South Indian": ["Masala Dosa", "Idli Sambar", "Vada", "Uttapam"],
    "Italian": ["Margherita Pizza", "Pasta Alfredo", "Garlic Bread", "Lasagna"],
    "Fast Food": ["Veg Burger", "French Fries", "Chicken Wrap", "Cold Coffee"],
    "Bakery": ["Chocolate Cake", "Croissant", "Brownie", "Cupcake"],
    "Desserts": ["Ice Cream Sundae", "Gulab Jamun", "Waffle", "Kulfi"],
    "Cafe": ["Cappuccino", "Cold Brew", "Club Sandwich", "Pancakes"],
}
DEFAULT_DISHES = ["Chef's Special", "House Combo", "Signature Platter", "Daily Special"]


def get_dishes_for_cuisine(cuisine_str):
    if not isinstance(cuisine_str, str):
        return DEFAULT_DISHES
    for tag, dishes in DISH_POOL.items():
        if tag.lower() in cuisine_str.lower():
            return dishes
    return DEFAULT_DISHES


def seed():
    df = pd.read_csv(CSV_PATH, encoding="latin-1")
    df = df.drop_duplicates(subset=["Restaurant Name"]).head(300)  # cap for manageable seed size

    app = create_app()
    with app.app_context():
        # Wipe existing seed data so this script is safely re-runnable
        MenuItem.query.delete()
        Restaurant.query.delete()
        db.session.commit()

        for _, row in df.iterrows():
            name = str(row.get("Restaurant Name", "")).strip()
            if not name:
                continue

            cuisine = str(row.get("Cuisines", "Multicuisine"))
            rating = row.get("Aggregate rating", 0.0)
            try:
                rating = float(rating)
            except (TypeError, ValueError):
                rating = 0.0

            restaurant = Restaurant(
                name=name,
                cuisine=cuisine,
                rating=rating,
            )
            db.session.add(restaurant)
            db.session.flush()  # get restaurant.id before inserting menu items

            dishes = get_dishes_for_cuisine(cuisine)
            avg_cost = row.get("Average Cost for two", 400)
            try:
                avg_cost = float(avg_cost)
            except (TypeError, ValueError):
                avg_cost = 400.0
            base_price = max(avg_cost / 2, 80)

            for dish_name in dishes:
                price = round(base_price * random.uniform(0.7, 1.3), 2)
                menu_item = MenuItem(
                    restaurant_id=restaurant.id,
                    name=dish_name,
                    category="Dessert" if dish_name in DISH_POOL.get("Desserts", []) else "Main",
                    price=price,
                    veg_flag=random.choice([True, False]),
                    cuisine_tags=cuisine,
                )
                db.session.add(menu_item)

        db.session.commit()
        print(f"Seeded {Restaurant.query.count()} restaurants and {MenuItem.query.count()} menu items.")


if __name__ == "__main__":
    seed()