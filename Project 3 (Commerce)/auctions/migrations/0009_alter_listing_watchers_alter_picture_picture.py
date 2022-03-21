# Generated by Django 4.0.2 on 2022-02-17 08:12

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0008_alter_picture_picture'),
    ]

    operations = [
        migrations.AlterField(
            model_name='listing',
            name='watchers',
            field=models.ManyToManyField(blank=True, related_name='watched_listings', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='picture',
            name='picture',
            field=models.ImageField(upload_to='images/'),
        ),
    ]