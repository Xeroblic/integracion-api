# Generated by Django 4.2.5 on 2024-05-12 07:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0013_remove_detallepedido_fecha'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pedido',
            name='iva',
            field=models.IntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='pedido',
            name='subtotal',
            field=models.IntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='pedido',
            name='total',
            field=models.IntegerField(null=True),
        ),
    ]