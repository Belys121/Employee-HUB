# Generated by Django 4.2.11 on 2024-09-25 18:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('viewer', '0009_contract_groups_subcontract_delete_project_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contract',
            name='status',
            field=models.CharField(choices=[('0', 'V procesu'), ('1', 'Dokončeno'), ('2', 'Zrušeno')], default=('0', 'V procesu'), max_length=64),
        ),
    ]
