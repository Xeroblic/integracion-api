# Generated by Django 4.2.5 on 2024-05-10 23:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0006_remove_producto_valor'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tipoestado',
            name='nombre',
            field=models.CharField(choices=[(1, 'Aceptado'), (2, 'En proceso'), (3, 'Enviado'), (4, 'Finalizado'), (5, 'Reembolsado'), (6, 'Pendiente de pago')], max_length=50),
        ),
    ]
