from io import BytesIO

from barcode import EAN13
from barcode.writer import ImageWriter
from django.core.files import File
from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.account.models import Employee
from apps.account.models import User


class Stock(models.Model):
    name = models.CharField(_("Lagername"), max_length=64)
    location = models.TextField(_("Standort"), max_length=500)
    manager = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="stocks", verbose_name="Lagerleitung"
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Lager"
        verbose_name_plural = "Lager"
        ordering = ("name",)


class Category(models.Model):
    name = models.CharField(_("Kategorie"), max_length=128)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _("Kategorie")
        verbose_name_plural = _("Kategorien")
        ordering = ("name",)


class Item(models.Model):
    class UnitChoices(models.IntegerChoices):
        PIECES = 1, _("Stück")
        METER = 2, _("Meter")
        ROLL = 3, _("Rolle")

    class ColorSelection(models.IntegerChoices):
        RED = 1, _("Rot")
        YELLOW = 2, _("Gelb")
        GREEN = 3, _("Grün")
        DEFAULT = 4, _("")

    name = models.CharField(_("Bezeichnung"), max_length=64)
    description = models.TextField(
        _("Beschreibung"), max_length=256, null=True, blank=True
    )
    image = models.ImageField(
        verbose_name=_("Artikelbild"),
        upload_to="image",
        null=True,
        blank=True,
        default="default-product-image.jpg",
    )
    manufacturer_number = models.CharField(
        _("Hersteller Artikelnummer"), max_length=64, blank=True
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name="products",
        blank=True,
        verbose_name=_("Kategorie"),
    )
    unit = models.PositiveSmallIntegerField(
        choices=UnitChoices.choices,
        default=UnitChoices.PIECES,
        verbose_name=_("Maßeinheit"),
    )
    favorite = models.PositiveSmallIntegerField(
        choices=ColorSelection.choices,
        default=ColorSelection.DEFAULT,
        verbose_name=_("Favorit"),
    )
    department = models.CharField(
        _("Abteilung"), max_length=64, blank=True, default="AC"
    )
    on_stock = models.PositiveSmallIntegerField(
        verbose_name=_("Lagerbestand"), default=0
    )
    min_stock = models.PositiveSmallIntegerField(
        verbose_name=_("Mindestbestand"), default=1
    )
    stock = models.ForeignKey(
        Stock,
        on_delete=models.CASCADE,
        related_name="items",
        verbose_name=_("Lager"),
    )
    ean = models.CharField(verbose_name=_("EAN"), max_length=13)
    barcode = models.ImageField(
        verbose_name=_("Strichcode"),
        # default="item/barcode/barcode.svg",
        upload_to="barcode",
        null=True,
        blank=True,
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Artikel"
        verbose_name_plural = "Artikeln"
        ordering = ("name",)

    def save(self, *args, **kwargs):
        if not self.barcode:
            ean = EAN13(str(self.ean), writer=ImageWriter())
            buffer = BytesIO()
            ean.write(buffer)
            self.barcode.save(f"barcode_{self.ean}.png", File(buffer), save=False)
        return super().save(*args, **kwargs)


class Order(models.Model):
    employee = models.ForeignKey(
        Employee, on_delete=models.PROTECT, verbose_name=Employee._meta.verbose_name
    )

    note = models.TextField(
        max_length=256, verbose_name=_("Notiz"), blank=True, null=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_("erstellt am"),
        editable=False,
    )
    modified_at = models.DateTimeField(
        verbose_name=_("geändert am"), editable=False, auto_now=True
    )

    class Meta:
        verbose_name = "Auftrag/ Entnahme"
        verbose_name_plural = "Aufträge/ Entnahme"
        ordering = ("created_at",)

    def __str__(self):
        return f"{self.employee} {self.created_at}"

    def get_total(self):
        return sum(item.quantity for item in self.items.all())


class OrderItem(models.Model):
    order = models.ForeignKey(
        Order, verbose_name=_("Auftrag"), on_delete=models.CASCADE, related_name="items"
    )
    item = models.ForeignKey(
        Item,
        verbose_name=_("Artikel"),
        on_delete=models.CASCADE,
        related_name="order_items",
    )
    quantity = models.PositiveSmallIntegerField(verbose_name=_("menge"), default=0)

    class Meta:
        verbose_name = "Artikel"
        verbose_name_plural = "Artikeln"

    def __str__(self):
        return str(self.id)


class ReturnRequest(models.Model):
    STATUS_CHOICES = (
        ("pending", "In Bearbeitung"),
        ("approved", "Bestätigt"),
        ("rejected", "Zurückgewiesen"),
    )
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, verbose_name="Mitarbeiter")
    reason = models.TextField(verbose_name=_("Rückgabegrund"))
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="pending")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(
        verbose_name=_("geändert am"), editable=False, auto_now=True
    )

    class Meta:
        verbose_name = "Retoure"
        verbose_name_plural = "Retoure"

    def __str__(self):
        return f"{self.employee} {self.created_at}"

    def save(self, *args, **kwargs):
        if self.status == "approved":
            for return_request_item in self.items.all():
                item = Item.objects.get(id=return_request_item.item_id)
                item.on_stock += return_request_item.quantity
                item.save()
        return super().save(*args, **kwargs)


class ReturnRequestItem(models.Model):
    return_request = models.ForeignKey(
        ReturnRequest,
        verbose_name=_("Retoure"),
        on_delete=models.CASCADE,
        related_name="items",
    )
    item = models.ForeignKey(
        Item,
        verbose_name=_("Artikel"),
        on_delete=models.CASCADE,
        related_name="return_request_items",
    )
    quantity = models.PositiveSmallIntegerField(verbose_name=_("menge"), default=0)

    class Meta:
        verbose_name = "Rückgabe Artikel"
        verbose_name_plural = "Rückgabe Artikeln"

    def __str__(self):
        return str(self.id)
