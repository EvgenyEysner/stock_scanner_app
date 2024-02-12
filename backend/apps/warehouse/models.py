from io import BytesIO

from barcode import EAN13
from barcode.writer import ImageWriter
from django.core.files import File
from django.db import models
from django.utils.translation import gettext_lazy as _


class Item(models.Model):
    class UnitChoices(models.IntegerChoices):
        PIECES = 1, _("Stück")
        METER = 2, _("Meter")
        ROLL = 3, _("Rolle")

    name = models.CharField(_("Bezeichnung"), max_length=64)
    description = models.TextField(
        _("Beschreibung"), max_length=256, null=True, blank=True
    )
    # Todo Herstellernummer,Lager
    image = models.ImageField(
        verbose_name=_("Artikelbild"), upload_to="item/image", null=True, blank=True
    )
    unit = models.PositiveSmallIntegerField(
        choices=UnitChoices.choices,
        default=UnitChoices.PIECES,
        verbose_name=_("Maßeinheit"),
    )

    stock = models.PositiveSmallIntegerField(verbose_name=_("Lagerbestand"), default=0)
    ean = models.CharField(verbose_name=_("EAN"), max_length=13)
    position_number = models.IntegerField(
        verbose_name=_("Position bei Hauptlager"), default=0
    )
    barcode = models.ImageField(
        verbose_name=_("Strichcode"),
        default="item/barcode/barcode.svg",
        upload_to="item/barcode",
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
