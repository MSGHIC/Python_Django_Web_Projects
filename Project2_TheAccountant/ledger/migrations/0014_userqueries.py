# Generated by Django 2.1.3 on 2019-01-06 08:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ledger', '0013_auto_20181121_2341'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserQueries',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('yourname', models.CharField(max_length=100)),
                ('email', models.EmailField(max_length=254)),
                ('subject', models.CharField(max_length=100)),
                ('message', models.TextField(max_length=255)),
            ],
        ),
    ]