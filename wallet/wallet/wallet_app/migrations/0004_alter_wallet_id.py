# Generated by Django 3.2.18 on 2023-04-21 07:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wallet_app', '0003_auto_20230421_0715'),
    ]

    operations = [
        migrations.AlterField(
            model_name='wallet',
            name='id',
            field=models.AutoField(db_column='wallet_id', max_length=10, primary_key=True, serialize=False),
        ),
    ]
