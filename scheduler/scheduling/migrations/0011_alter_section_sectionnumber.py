# Generated by Django 4.2 on 2023-07-24 08:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('scheduling', '0010_section'),
    ]

    operations = [
        migrations.AlterField(
            model_name='section',
            name='sectionnumber',
            field=models.CharField(max_length=20),
        ),
    ]