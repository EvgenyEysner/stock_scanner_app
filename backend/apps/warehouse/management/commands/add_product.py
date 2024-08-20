import csv

from django.core.management.base import BaseCommand

from apps.warehouse.models import Category, Item


def get_unit(row):
    if row == "Stück":
        unit = 1

    if row == "Meter":
        unit = 2

    if row == "Rolle":
        unit = 3
    return unit


class Command(BaseCommand):
    help = "Add products"

    # def add_arguments(self, parser): ...

    def handle(self, *args, **options):
        # file = str(input("Dateipfad eingeben: "))
        file = "../backend/bedarfsliste_08_2024.csv"

        with open(file, encoding="UTF-8") as f:
            reader = csv.DictReader(f, delimiter=",")

            units = ["Stück", "Meter", "Rolle"]
            for row in reader:

                if row["EAN"].isdigit() and len(row["EAN"]) == 13 and row["EAN"] != "":
                    ean = row["EAN"]

                if row["Kategorie"] is not None:
                    name = row["Kategorie"]

                if row["Hersteller Artikelnummer"] != "":
                    manufacturer_number = row["Hersteller Artikelnummer"]

                    unit = get_unit(row["Maßeinheit"])

                    Item.objects.create(
                        name=row["Material"],
                        manufacturer_number=manufacturer_number,
                        category_id=Category.objects.get(name=name).id,
                        stock_id=1,
                        image="default-product-image.png",
                        unit=unit,
                        ean=ean,
                        on_stock=10,
                        position_number=row["Pos."],
                    )
