# Generated by Django 4.1.7 on 2023-04-23 18:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("clientes", "0008_alter_cliente_id_restaurante"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="cliente",
            name="id_restaurante",
        ),
        migrations.AlterField(
            model_name="cliente",
            name="cedula",
            field=models.CharField(max_length=20, unique=True),
        ),
    ]
