# Generated by Django 4.2.3 on 2023-12-08 13:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payment', '0002_remove_payment_description_alter_payment_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='payment',
            name='braintree_id',
            field=models.CharField(blank=True, max_length=150, null=True),
        ),
    ]
