# Generated by Django 4.1.7 on 2023-03-30 16:01

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Restaurante",
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
                ("nombre", models.CharField(max_length=100)),
                ("NIT", models.CharField(max_length=20)),
                ("direccion", models.CharField(max_length=200)),
                ("telefono", models.CharField(max_length=20)),
                ("tipo", models.CharField(max_length=100)),
            ],
        ),
    ]
