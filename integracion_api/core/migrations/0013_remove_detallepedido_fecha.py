# Generated by Django 4.2.5 on 2024-05-12 06:50

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0012_rename_id_pedido_detallepedido_pedido_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='detallepedido',
            name='fecha',
        ),
    ]
