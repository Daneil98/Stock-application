# Generated by Django 4.2.3 on 2023-12-05 14:35

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0009_remove_payment_amount'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='payment',
            name='CVV',
        ),
        migrations.RemoveField(
            model_name='payment',
            name='Card_Number',
        ),
        migrations.RemoveField(
            model_name='payment',
            name='Expiration_date',
        ),
    ]
