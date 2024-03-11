import csv
from django.core.management.base import BaseCommand

from apps.warehouse.models import Category, Item


def add_category(file):
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


def add_products(file):
    with open(file, encoding="UTF-8") as f:
        reader = csv.DictReader(f, delimiter=",")

        for row in reader:
            category = Category.objects.filter(name=row["Kategorie"]).first()
            print(category)
            if row["EAN"].isdigit() and len(row["EAN"]) == 13:
                ean = row["EAN"]

            if row["Maßeinheit"] == "Rolle":
                unit = 3
                Item.objects.create(
                    name=row["Material"],
                    manufacturer_number=row["Hersteller Artikelnummer"],
                    category_id=Category.objects.get(name=row["Kategorie"]).id,
                    stock_id=1,
                    unit=unit,
                    ean=ean,
                    on_stock=10,
                    position_number=row["Pos."]
                )


class Command(BaseCommand):
    help = "Add products"

    def add_arguments(self, parser): ...

    def handle(self, *args, **options):
        # file = str(input("Dateipfad eingeben: "))
        file = "../backend/Bedarfsliste.csv"

        # add_category(file)
        add_products(file)
        # with open(file, encoding="UTF-8") as f:
        #     reader = csv.DictReader(f, delimiter=",")
        # for row in reader:
        #     print(row["Kategorie"])
