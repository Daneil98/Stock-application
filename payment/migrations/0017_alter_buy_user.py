# Generated by Django 4.2.3 on 2024-01-07 15:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payment', '0016_amount'),
    ]

    operations = [
        migrations.AlterField(
            model_name='buy',
            name='user',
            field=models.CharField(max_length=200, null=True),
        ),
    ]