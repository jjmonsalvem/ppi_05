# Generated by Django 4.1.7 on 2023-04-19 21:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("clientes", "0004_alter_cliente_id_restaurante_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="cliente",
            name="cedula",
            field=models.CharField(max_length=20, unique=True),
        ),
    ]