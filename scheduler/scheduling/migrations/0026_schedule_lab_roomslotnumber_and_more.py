# Generated by Django 4.2 on 2023-08-16 05:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('scheduling', '0025_rename_laboratory_building_number_schedule_lab_building_number_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='schedule',
            name='lab_roomslotnumber',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
        migrations.AddField(
            model_name='schedule',
            name='lecture_roomslotnumber',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
    ]