# Generated by Django 4.2 on 2023-11-27 09:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('scheduling', '0037_alter_courselist_college'),
    ]

    operations = [
        migrations.AddField(
            model_name='college',
            name='semester',
            field=models.CharField(blank=True, default='First Semester', max_length=100),
        ),
    ]
