# Generated by Django 4.2 on 2023-07-27 16:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('scheduling', '0011_alter_section_sectionnumber'),
    ]

    operations = [
        migrations.AddField(
            model_name='course',
            name='college',
            field=models.CharField(blank=True, max_length=100),
        ),
    ]
