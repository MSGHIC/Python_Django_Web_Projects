# Generated by Django 2.1.3 on 2018-11-21 15:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ledger', '0012_auto_20181121_1458'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bills_update',
            name='count',
            field=models.PositiveIntegerField(default=0),
        ),
    ]
