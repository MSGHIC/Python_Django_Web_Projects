# Generated by Django 2.1.3 on 2019-04-06 14:45

import cloudinary.models
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ledger', '0017_remove_company_site_video'),
    ]

    operations = [
        migrations.AddField(
            model_name='company',
            name='site_video',
            field=cloudinary.models.CloudinaryField(default='media/uploads/video.mp4', max_length=255),
        ),
    ]
