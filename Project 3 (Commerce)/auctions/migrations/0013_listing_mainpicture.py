# Generated by Django 4.0.2 on 2022-02-21 13:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0012_alter_picture_picture'),
    ]

    operations = [
        migrations.AddField(
            model_name='listing',
            name='mainPicture',
            field=models.ImageField(blank=True, null=True, upload_to=''),
        ),
    ]
