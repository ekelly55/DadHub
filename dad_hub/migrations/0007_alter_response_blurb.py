# Generated by Django 4.1.2 on 2022-10-10 17:26

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('dad_hub', '0006_response_content'),
    ]

    operations = [
        migrations.AlterField(
            model_name='response',
            name='blurb',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='responses', to='dad_hub.blurb'),
        ),
    ]
