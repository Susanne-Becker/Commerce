# Generated by Django 3.2 on 2021-04-25 09:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0006_auto_20210425_0938'),
    ]

    operations = [
        migrations.AddField(
            model_name='listing',
            name='winner',
            field=models.CharField(blank=True, default=None, max_length=50, null=True),
        ),
    ]
