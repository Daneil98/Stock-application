# Generated by Django 4.2 on 2024-10-15 13:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0018_remove_profile_pin_profile_secret_key'),
    ]

    operations = [
        migrations.AddField(
            model_name='price_db',
            name='user',
            field=models.CharField(max_length=200, null=True),
        ),
    ]
