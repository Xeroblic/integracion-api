# Generated by Django 4.2.5 on 2024-05-12 09:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0017_rename_id_usuario_pedido_usuario'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pedido',
            name='fecha',
            field=models.DateField(),
        ),
    ]
