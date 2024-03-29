# Generated by Django 4.2.3 on 2024-01-05 22:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payment', '0012_buy_balance'),
    ]

    operations = [
        migrations.RenameField(
            model_name='buy',
            old_name='purchase_amount',
            new_name='stock_purchase_price',
        ),
        migrations.AddField(
            model_name='buy',
            name='total_purchase_price',
            field=models.DecimalField(decimal_places=2, max_digits=10, null=True),
        ),
    ]
