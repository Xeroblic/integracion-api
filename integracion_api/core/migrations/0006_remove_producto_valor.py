# Generated by Django 4.2.5 on 2024-05-10 23:50

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0005_estado_tipoestado_rename_precio_producto_precio_neto_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='producto',
            name='valor',
        ),
    ]