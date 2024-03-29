# Generated by Django 4.2 on 2023-11-28 18:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0003_payment_remove_transaction_owner_delete_account_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='payment',
            name='braintree_id',
            field=models.CharField(blank=True, max_length=150),
        ),
        migrations.AddField(
            model_name='profile',
            name='address',
            field=models.CharField(blank=True, max_length=120),
        ),
        migrations.AddField(
            model_name='profile',
            name='phone',
            field=models.IntegerField(null=True, unique=True),
        ),
        migrations.AlterField(
            model_name='payment',
            name='id',
            field=models.AutoField(primary_key=True, serialize=False),
        ),
    ]
