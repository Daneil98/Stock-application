# Generated by Django 4.2.3 on 2023-12-08 16:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payment', '0006_remove_payment_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='payment',
            name='amount',
            field=models.IntegerField(null=True),
        ),
    ]
