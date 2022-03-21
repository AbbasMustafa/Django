# Generated by Django 4.0.2 on 2022-02-22 18:22

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0013_listing_mainpicture'),
    ]

    operations = [
        migrations.AlterField(
            model_name='listing',
            name='buyers',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='buyers_lisitng', to=settings.AUTH_USER_MODEL),
        ),
    ]
