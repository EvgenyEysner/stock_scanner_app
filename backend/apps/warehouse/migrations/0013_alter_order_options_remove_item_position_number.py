# Generated by Django 4.1.3 on 2024-09-06 06:49

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("warehouse", "0012_alter_item_barcode"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="order",
            options={
                "ordering": ("created_at",),
                "verbose_name": "Auftrag/ Entnahme",
                "verbose_name_plural": "Aufträge/ Entnahme",
            },
        ),
        migrations.RemoveField(
            model_name="item",
            name="position_number",
        ),
    ]
