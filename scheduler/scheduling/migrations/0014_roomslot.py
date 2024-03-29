# Generated by Django 4.2 on 2023-07-30 16:33

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('scheduling', '0013_timeslot'),
    ]

    operations = [
        migrations.CreateModel(
            name='RoomSlot',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('roomslottype', models.CharField(max_length=50)),
                ('day', models.CharField(max_length=20)),
                ('building_number', models.CharField(max_length=20)),
                ('roomname', models.CharField(max_length=100)),
                ('starttime', models.TimeField()),
                ('endtime', models.TimeField()),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='scheduling.course')),
                ('room', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='scheduling.room')),
                ('timeslot', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='scheduling.timeslot')),
            ],
        ),
    ]
