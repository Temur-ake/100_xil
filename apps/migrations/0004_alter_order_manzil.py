# Generated by Django 5.1.1 on 2024-11-26 06:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('apps', '0003_order_manzil_order_talab'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='manzil',
            field=models.TextField(blank=True, null=True, verbose_name='Manzil'),
        ),
    ]
