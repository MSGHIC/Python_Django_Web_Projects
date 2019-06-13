# Generated by Django 2.1 on 2018-09-30 02:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ledger', '0005_auto_20180930_0157'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='loan',
            name='approved',
        ),
        migrations.AddField(
            model_name='approveloan',
            name='remarks',
            field=models.CharField(default='In_Review', max_length=20),
        ),
        migrations.AddField(
            model_name='approveloan',
            name='status',
            field=models.CharField(default='In_Review', max_length=20),
        ),
        migrations.AddField(
            model_name='loan',
            name='status',
            field=models.CharField(default='In_Review', max_length=20),
        ),
        migrations.AlterField(
            model_name='approveloan',
            name='approved',
            field=models.CharField(choices=[('IR', 'In-Review'), ('AP', 'Approved'), ('RJ', 'Rejected')], default='select', max_length=20),
        ),
    ]
