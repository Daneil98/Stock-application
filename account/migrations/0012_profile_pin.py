# Generated by Django 4.2.3 on 2023-12-08 15:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0011_delete_payment'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='PIN',
            field=models.CharField(max_length=4, null=True),
        ),
    ]
