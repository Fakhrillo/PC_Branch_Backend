# Generated by Django 5.0.1 on 2024-02-05 09:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='camera_details',
            name='stream_link',
            field=models.URLField(blank=True, max_length=100, null=True),
        ),
    ]
