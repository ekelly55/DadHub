# Generated by Django 4.1.2 on 2022-10-08 11:46

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('dad_hub', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='blurb',
            name='user',
        ),
    ]