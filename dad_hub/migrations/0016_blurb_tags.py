# Generated by Django 4.1.2 on 2022-10-12 20:46

import django.contrib.postgres.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dad_hub', '0015_blurb_image_blurb_link'),
    ]

    operations = [
        migrations.AddField(
            model_name='blurb',
            name='tags',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.CharField(blank=True, max_length=20), default=list, size=None),
        ),
    ]