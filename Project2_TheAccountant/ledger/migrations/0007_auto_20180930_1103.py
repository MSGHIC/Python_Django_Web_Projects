# Generated by Django 2.1 on 2018-09-30 03:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ledger', '0006_auto_20180930_1053'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='approveloan',
            name='approved',
        ),
        migrations.AlterField(
            model_name='approveloan',
            name='status',
            field=models.CharField(choices=[('IR', 'In-Review'), ('AP', 'Approved'), ('RJ', 'Rejected')], default='select', max_length=20),
        ),
    ]
