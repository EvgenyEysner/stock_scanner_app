# Generated by Django 4.1.3 on 2024-09-09 15:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("warehouse", "0013_alter_order_options_remove_item_position_number"),
    ]

    operations = [
        migrations.AddField(
            model_name="item",
            name="min_stock",
            field=models.PositiveSmallIntegerField(
                default=1, verbose_name="Mindestbestand"
            ),
        ),
    ]
