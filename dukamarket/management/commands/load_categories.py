from django.core.management.base import BaseCommand
from app.models import MainCategory, Category, SubCategory


class Command(BaseCommand):
    help = "Load Amazon-style categories (3-level) into the database"

    def handle(self, *args, **options):
        categories_data = {
            "Mobiles & Accessories": {
                "Smartphones": ["Android Phones", "iPhones", "Gaming Phones"],
                "Feature Phones": ["Basic Phones", "Dual SIM Phones", "Senior-Friendly Phones"],
                "Power Banks": ["Fast Charging", "Solar Power Banks", "High Capacity"],
                "Cases & Covers": ["Back Covers", "Flip Covers", "Rugged Cases"],
                "Chargers & Cables": ["Wall Chargers", "Wireless Chargers", "USB Cables"],
                "Mobile Audio": ["Wired Earphones", "Bluetooth Earbuds", "Headsets"],
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
