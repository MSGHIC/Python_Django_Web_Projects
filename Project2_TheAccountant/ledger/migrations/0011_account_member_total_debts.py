# Generated by Django 2.1 on 2018-10-07 14:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ledger', '0010_auto_20181007_2243'),
    ]

    operations = [
        migrations.AddField(
            model_name='account',
            name='member_total_debts',
            field=models.PositiveIntegerField(default=0),
        ),
    ]
