# Generated by Django 2.1.3 on 2019-01-06 08:49

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ledger', '0014_userqueries'),
    ]

    operations = [
        migrations.RenameField(
            model_name='userqueries',
            old_name='yourname',
            new_name='name',
        ),
    ]
