# Generated by Django 2.1.1 on 2018-09-21 07:31

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0003_auto_20180920_2328'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='serviceinstance',
            name='duration',
        ),
    ]
