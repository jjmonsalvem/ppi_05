# Generated by Django 4.1.7 on 2023-03-30 16:01

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("restaurantes", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Cliente",
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
                ("cedula", models.CharField(max_length=20)),
                ("telefono", models.CharField(max_length=20)),
                (
                    "id_restaurante",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="restaurantes.restaurante",
                    ),
                ),
            ],
        ),
    ]
