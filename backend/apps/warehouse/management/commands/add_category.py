import csv

from django.core.management.base import BaseCommand

from apps.warehouse.models import Category


class Command(BaseCommand):
    help = "Add product category"

    def handle(self, *args, **options):
        file = "../backend/bedarfsliste_08_2024.csv"
        with open(file, encoding="UTF-8") as f:
            reader = csv.DictReader(f, delimiter=",")
            category = set()
            try:
                for row in reader:
                    if (
                        row["Kategorie"] in category
                        or row["Kategorie"] == "#WERT!"
                        or row["Kategorie"].isdigit()
                        or row["Kategorie"] == ""
                    ):
                        continue
                    category.add(row["Kategorie"].replace(" ", ""))
                for name in category:
                    Category.objects.create(name=name)
            except Exception as e:
                print(row, e)
