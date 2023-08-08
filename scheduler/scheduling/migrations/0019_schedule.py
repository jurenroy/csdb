# Generated by Django 4.2 on 2023-08-08 08:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('scheduling', '0018_alter_roomslot_roomslotnumber'),
    ]

    operations = [
        migrations.CreateModel(
            name='Schedule',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('course', models.CharField(max_length=100)),
                ('section', models.CharField(max_length=50)),
                ('subject', models.CharField(max_length=100)),
                ('instructor', models.CharField(blank=True, max_length=100, null=True)),
                ('lecture_day', models.CharField(blank=True, max_length=20, null=True)),
                ('lecture_time', models.CharField(blank=True, max_length=50, null=True)),
                ('lecture_room', models.CharField(blank=True, max_length=50, null=True)),
                ('lab_day', models.CharField(blank=True, max_length=20, null=True)),
                ('lab_time', models.CharField(blank=True, max_length=50, null=True)),
                ('lab_room', models.CharField(blank=True, max_length=50, null=True)),
            ],
        ),
    ]
