# Generated by Django 3.2.5 on 2021-08-02 14:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0005_listing_winner'),
    ]

    operations = [
        migrations.AddField(
            model_name='listing',
            name='closed',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]