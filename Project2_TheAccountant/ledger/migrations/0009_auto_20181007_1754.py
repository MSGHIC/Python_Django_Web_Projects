# Generated by Django 2.1 on 2018-10-07 09:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ledger', '0008_auto_20180930_1109'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='loan',
            name='name',
        ),
        migrations.AddField(
            model_name='loan',
            name='reason',
            field=models.TextField(default='State cause for borrowing and How you plan to pay back.', max_length=255),
        ),
        migrations.AlterField(
            model_name='account',
            name='member_capital',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='approveloan',
            name='remarks',
            field=models.TextField(default='Good luck with the loan, remember to be a responsible Borrower and pay in time....Chief Accountant'),
        ),
    ]
