# Generated by Django 4.1.3 on 2024-04-23 18:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("warehouse", "0010_alter_order_employee"),
    ]

    operations = [
        migrations.AlterField(
            model_name="order",
            name="note",
            field=models.TextField(
                blank=True, max_length=256, null=True, verbose_name="Notiz"
            ),
        ),
    ]