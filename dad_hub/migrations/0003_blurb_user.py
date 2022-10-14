# Generated by Django 4.1.2 on 2022-10-09 15:50

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('dad_hub', '0002_remove_blurb_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='blurb',
            name='user',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
