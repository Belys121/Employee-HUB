# Generated by Django 4.1.1 on 2024-10-09 14:53

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('viewer', '0012_alter_contract_deadline'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contract',
            name='deadline',
            field=models.DateTimeField(default=datetime.datetime(2024, 11, 8, 16, 53, 1, 379990)),
        ),
    ]