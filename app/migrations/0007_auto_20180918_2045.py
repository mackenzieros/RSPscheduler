# Generated by Django 2.1.1 on 2018-09-19 03:45

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0006_schedule_teacher'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='service',
            options={'permissions': (('can_view_service', 'Can view service'),)},
        ),
        migrations.AlterModelOptions(
            name='student',
            options={'ordering': ['last_name', 'first_name'], 'permissions': (('can_view_student', 'Can view student'),)},
        ),
    ]
