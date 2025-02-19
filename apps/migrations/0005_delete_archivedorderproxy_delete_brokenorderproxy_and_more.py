# Generated by Django 5.1.1 on 2024-11-26 07:21

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('apps', '0004_alter_order_manzil'),
    ]

    operations = [
        migrations.DeleteModel(
            name='ArchivedOrderProxy',
        ),
        migrations.DeleteModel(
            name='BrokenOrderProxy',
        ),
        migrations.DeleteModel(
            name='CanceledOrderProxy',
        ),
        migrations.DeleteModel(
            name='ReadyToDeliverOrderProxy',
        ),
        migrations.DeleteModel(
            name='ReturnedOrderProxy',
        ),
        migrations.DeleteModel(
            name='WaitingOrderProxy',
        ),
        migrations.CreateModel(
            name='FreshStatisticProxy',
            fields=[
            ],
            options={
                'verbose_name': 'Fresh food Statistikasi',
                'verbose_name_plural': 'Fresh food Statistikalari',
                'proxy': True,
                'indexes': [],
                'constraints': [],
            },
            bases=('apps.order',),
        ),
        migrations.AlterField(
            model_name='order',
            name='owner',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='orders', to=settings.AUTH_USER_MODEL, verbose_name='Owner'),
        ),
    ]
