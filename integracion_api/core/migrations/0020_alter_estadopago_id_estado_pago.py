# Generated by Django 4.2.5 on 2024-05-13 00:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0019_metodopago_descripcion_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='estadopago',
            name='id_estado_pago',
            field=models.IntegerField(primary_key=True, serialize=False),
        ),
    ]
