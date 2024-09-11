# Generated by Django 5.1.1 on 2024-09-09 14:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('apps', '0005_order_discount'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='discount',
        ),
        migrations.AddField(
            model_name='product',
            name='discount',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
