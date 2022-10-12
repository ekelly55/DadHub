# Generated by Django 4.1.2 on 2022-10-12 15:26

from django.conf import settings
import django.contrib.postgres.fields
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('dad_hub', '0011_delete_profile'),
    ]

    operations = [
        migrations.CreateModel(
            name='Bio',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('picture', models.CharField(max_length=200)),
                ('state', models.CharField(max_length=2)),
                ('county', models.CharField(max_length=20)),
                ('zip', models.CharField(max_length=5)),
                ('kids_ages', django.contrib.postgres.fields.ArrayField(base_field=models.CharField(max_length=2), size=None)),
                ('interests', django.contrib.postgres.fields.ArrayField(base_field=models.CharField(max_length=10), size=None)),
                ('bio', models.TextField(max_length=200)),
                ('user', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]