# Generated by Django 4.2.3 on 2023-12-20 23:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payment', '0009_alter_payment_amount'),
    ]

    operations = [
        migrations.CreateModel(
            name='Buy',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, null=True)),
                ('purchase_amount', models.DecimalField(decimal_places=2, max_digits=10)),
                ('bought', models.BooleanField(default=False)),
                ('shares', models.CharField(max_length=10, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Sell',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, null=True)),
                ('selling_amount', models.DecimalField(decimal_places=2, max_digits=10)),
                ('sold', models.BooleanField(default=False)),
                ('shares', models.CharField(max_length=10, null=True)),
            ],
        ),
        migrations.AlterField(
            model_name='payment',
            name='amount',
            field=models.DecimalField(decimal_places=2, default=100, max_digits=10),
        ),
    ]