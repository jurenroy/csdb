# Generated by Django 4.2 on 2023-07-21 05:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('scheduling', '0006_room_roomtype'),
    ]

    operations = [
        migrations.AlterField(
            model_name='course',
            name='abbreviation',
            field=models.CharField(blank=True, max_length=20),
        ),
        migrations.AddConstraint(
            model_name='course',
            constraint=models.UniqueConstraint(fields=('abbreviation',), name='unique_course_abbreviation'),
        ),
    ]
