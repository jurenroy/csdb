# Generated by Django 4.2 on 2023-08-08 08:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('scheduling', '0021_alter_schedule_section_alter_schedule_subject'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='schedule',
            name='section',
        ),
        migrations.RemoveField(
            model_name='schedule',
            name='subject',
        ),
        migrations.AddField(
            model_name='schedule',
            name='section_number',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
        migrations.AddField(
            model_name='schedule',
            name='section_year',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
        migrations.AddField(
            model_name='schedule',
            name='subject_code',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
        migrations.AddField(
            model_name='schedule',
            name='subject_name',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
