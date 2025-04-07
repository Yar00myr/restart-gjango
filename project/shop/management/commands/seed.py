import random
from faker import Faker
from django.core.management.base import BaseCommand
from shop.models import Category, Product


class Command(BaseCommand):

    _help = "Generates test data for databases"

    def handle(self, *args, **options):
        fake = Faker()

        categories = ["Baits", "Rods", "Reels", "Lures", "Tools"]
        categories_objects = [
            Category.objects.get_or_create(name=c)[0] for c in categories
        ]

        Product.objects.all().delete()

        for _ in range(50):
            Product.objects.create(
                name=fake.unique.word().capitalize(),
                category=random.choice(categories_objects),
                nomenclature=fake.unique.uuid4(),
                description=fake.text(max_nb_chars=100),
                price=random.randint(1, 100),
                discount=random.randint(1, 51),
                available=random.choice([True, False]),
                entity=random.randint(1, 1000),
                rating=round(random.uniform(0.1, 5.0), 1),
                attributes={"colour": fake.color_name()},
            )

        self.stdout.write(self.style.SUCCESS("Successfully addd 50 products"))
