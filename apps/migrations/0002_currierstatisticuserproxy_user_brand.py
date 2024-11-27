# Generated by Django 5.1.1 on 2024-11-26 04:28

import apps.models.proxy_managers
import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('apps', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='CurrierStatisticUserProxy',
            fields=[
            ],
            options={
                'verbose_name': 'Currier Statistics',
                'verbose_name_plural': 'Currier Statistics',
                'proxy': True,
                'indexes': [],
                'constraints': [],
            },
            bases=('apps.user',),
            managers=[
                ('objects', apps.models.proxy_managers.CurrierUserManager()),
            ],
        ),
        migrations.AddField(
            model_name='user',
            name='brand',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Currierning Brandi'),
        ),
    ]
