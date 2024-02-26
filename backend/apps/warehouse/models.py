from io import BytesIO

from barcode import EAN13
from barcode.writer import ImageWriter
from django.core.files import File
from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.account.models import User


class Stock(models.Model):
    name = models.CharField(_("Lagername"), max_length=64)
    location = models.TextField(_("Standort"), max_length=500)
    manager = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name="stocks"
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

    name = models.CharField(_("Bezeichnung"), max_length=64)
    description = models.TextField(
        _("Beschreibung"), max_length=256, null=True, blank=True
    )
    image = models.ImageField(
        verbose_name=_("Artikelbild"), upload_to="image", null=True, blank=True
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

    on_stock = models.PositiveSmallIntegerField(
        verbose_name=_("Lagerbestand"), default=0
    )
    stock = models.ForeignKey(
        Stock, on_delete=models.CASCADE, related_name="items", verbose_name=_("Lager")
    )
    ean = models.CharField(verbose_name=_("EAN"), max_length=13)
    position_number = models.IntegerField(
        verbose_name=_("Position bei Hauptlager"), default=0
    )
    barcode = models.ImageField(
        verbose_name=_("Strichcode"),
        default="item/barcode/barcode.svg",
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
        ean = EAN13(str(self.ean), writer=ImageWriter())
        buffer = BytesIO()
        ean.write(buffer)
        self.barcode.save(f"barcode_{self.ean}.png", File(buffer), save=False)
        return super().save(*args, **kwargs)
