# Generated by Django 4.2 on 2023-11-26 16:39

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('scheduling', '0033_alter_course_college'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='course',
            name='college',
        ),
    ]
