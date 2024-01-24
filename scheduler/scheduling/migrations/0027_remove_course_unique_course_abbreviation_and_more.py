# Generated by Django 4.2 on 2023-08-23 07:50

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('scheduling', '0026_schedule_lab_roomslotnumber_and_more'),
    ]

    operations = [
        migrations.RemoveConstraint(
            model_name='course',
            name='unique_course_abbreviation',
        ),
        migrations.AlterField(
            model_name='room',
            name='course',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='scheduling.course'),
        ),
        migrations.AlterField(
            model_name='schedule',
            name='course',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='scheduling.course'),
        ),
        migrations.AlterField(
            model_name='section',
            name='course',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='scheduling.course'),
        ),
        migrations.AlterField(
            model_name='subject',
            name='course',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='scheduling.course'),
        ),
        migrations.AlterField(
            model_name='timeslot',
            name='course',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='scheduling.course'),
        ),
    ]