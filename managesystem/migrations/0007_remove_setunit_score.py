# Generated by Django 4.2.6 on 2023-11-07 15:04

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("managesystem", "0006_remove_setunit_employeeposition_setunit_position"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="setunit",
            name="score",
        ),
    ]