# Generated by Django 4.2 on 2025-03-29 22:45

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='comment',
            options={'ordering': ('created',)},
        ),
        migrations.RemoveField(
            model_name='comment',
            name='email',
        ),
    ]
