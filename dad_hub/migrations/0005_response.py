# Generated by Django 4.1.2 on 2022-10-10 17:05

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('dad_hub', '0004_remove_blurb_name'),
    ]

    operations = [
        migrations.CreateModel(
            name='Response',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('blurb', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='dad_hub.blurb')),
                ('response', models.ManyToManyField(to='dad_hub.response')),
                ('user', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
