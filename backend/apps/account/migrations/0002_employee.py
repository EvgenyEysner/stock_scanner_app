# Generated by Django 4.1.3 on 2024-03-19 06:54

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("account", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Employee",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "created_on",
                    models.DateField(auto_now_add=True, verbose_name="Erstellt am"),
                ),
                (
                    "first_name",
                    models.CharField(max_length=255, verbose_name="Vorname"),
                ),
                (
                    "last_name",
                    models.CharField(max_length=255, verbose_name="Nachname"),
                ),
                ("street", models.CharField(max_length=255, verbose_name="Straße")),
                (
                    "street_no",
                    models.CharField(
                        blank=True, max_length=255, verbose_name="Hausnummer"
                    ),
                ),
                ("zip_code", models.CharField(max_length=5, verbose_name="PLZ")),
                ("city", models.CharField(max_length=255, verbose_name="Ort")),
                (
                    "permission_group",
                    models.PositiveSmallIntegerField(
                        choices=[
                            (1, "Monteur"),
                            (2, "Teamleitung"),
                            (3, "Lagerleitung"),
                            (4, "Backoffice"),
                        ],
                        default=4,
                        verbose_name="Berechtigungsgruppe",
                    ),
                ),
                (
                    "phone_mobile",
                    models.CharField(
                        blank=True, max_length=255, null=True, verbose_name="Handy"
                    ),
                ),
                ("date_of_birth", models.DateField(verbose_name="Geburtsdatum")),
                (
                    "date_of_joining",
                    models.DateField(
                        blank=True, null=True, verbose_name="Eintrittsdatum"
                    ),
                ),
                (
                    "date_of_leaving",
                    models.DateField(
                        blank=True, null=True, verbose_name="Austrittsdatum"
                    ),
                ),
                ("is_qualified", models.BooleanField(verbose_name="Qualifiziert?")),
                (
                    "date_of_qualification",
                    models.DateField(
                        blank=True,
                        null=True,
                        verbose_name="Zeitpunkt der Qualifizierung",
                    ),
                ),
                (
                    "user",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="employee",
                        to=settings.AUTH_USER_MODEL,
                        verbose_name="Nutzer:in",
                    ),
                ),
            ],
            options={
                "verbose_name": "Mitarbeiter",
                "verbose_name_plural": "Mitarbeiter",
                "ordering": ["last_name"],
            },
        ),
    ]