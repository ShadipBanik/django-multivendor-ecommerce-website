from django.core.management.base import BaseCommand
from app.models import MainCategory, Category, SubCategory


class Command(BaseCommand):
    help = "Load Amazon-style categories (3-level) into the database"

    def handle(self, *args, **options):
        categories_data = {
            "Electronics": {
                "Televisions": ["LED TVs", "OLED TVs", "Smart TVs", "4K TVs"],
                "Audio Equipment": ["Headphones", "Speakers", "Soundbars", "Home Theater Systems"],
                "Wearable Tech": ["Smartwatches", "Fitness Trackers", "VR Headsets", "Smart Glasses"],
                "Gaming Consoles": ["PlayStation", "Xbox", "Nintendo Switch", "Retro Consoles"],
                "Computer Accessories": ["Keyboards", "Mice", "Webcams", "Monitors"],
                "Networking": ["Routers", "Modems", "Wi-Fi Extenders", "Network Cables"],
            },
            "Books": {
                "Graphic Novels": ["Superhero Comics", "Manga", "Fantasy Comics", "Sci-Fi Comics"],
                "Cookbooks": ["Baking", "Healthy Recipes", "Regional Cuisine", "Quick Meals"],
                "Self-Improvement": ["Motivation", "Productivity", "Mindfulness", "Leadership"],
                "Travel Guides": ["Europe", "Asia", "North America", "Adventure Travel"],
                "Art & Photography": ["Painting", "Photography Techniques", "Sketching", "Digital Art"],
                "Science & Technology": ["Astronomy", "Physics", "Robotics", "Computer Science"],
            },
            "Home & Kitchen": {
                "Storage & Organization": ["Closet Organizers", "Storage Bins", "Shelving Units", "Hooks & Hangers"],
                "Home Decor": ["Wall Art", "Clocks", "Vases", "Candles"],
                "Cleaning Supplies": ["Vacuum Cleaners", "Mops & Brooms", "Cleaning Chemicals", "Microfiber Cloths"],
                "Lighting": ["Table Lamps", "Ceiling Lights", "LED Strips", "Outdoor Lights"],
                "Cookware & Utensils": ["Pots & Pans", "Knives", "Cutting Boards", "Cooking Utensils"],
                "Smart Home": ["Smart Lights", "Smart Plugs", "Smart Thermostats", "Security Cameras"],
            },
            "Clothing, Shoes & Jewelry": {
                "Men’s Shoes": ["Sneakers", "Formal Shoes", "Boots", "Sandals"],
                "Women’s Shoes": ["Heels", "Flats", "Boots", "Sneakers"],
                "Men’s Accessories": ["Belts", "Wallets", "Hats", "Sunglasses"],
                "Women’s Accessories": ["Scarves", "Handbags", "Jewelry Sets", "Hats"],
                "Men’s Clothing": ["T-Shirts", "Jeans", "Jackets", "Sweaters"],
                "Women’s Clothing": ["Dresses", "Tops", "Skirts", "Jumpsuits"],
            },
        }

        for main_name, cats in categories_data.items():
            main_category, _ = MainCategory.objects.get_or_create(name=main_name)
            for cat_name, subs in cats.items():
                category, _ = Category.objects.get_or_create(
                    main_category=main_category, name=cat_name
                )
                for sub_name in subs:
                    SubCategory.objects.get_or_create(category=category, name=sub_name)

        self.stdout.write(
            self.style.SUCCESS("✅ Main categories, categories, and subcategories loaded successfully!")
        )
