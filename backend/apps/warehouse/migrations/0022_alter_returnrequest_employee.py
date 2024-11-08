# Generated by Django 4.1.3 on 2024-10-17 05:41

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("account", "0003_alter_user_options_alter_employee_user"),
        ("warehouse", "0021_alter_stock_manager"),
    ]

    operations = [
        migrations.AlterField(
            model_name="returnrequest",
            name="employee",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                to="account.employee",
                verbose_name="Mitarbeiter",
            ),
        ),
    ]
