# Generated by Django 4.2.7 on 2023-11-21 09:09

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("managesystem", "0018_remove_save_employee_save_employee_firstname_and_more"),
    ]

    operations = [
        migrations.RenameField(
            model_name="save",
            old_name="employee_firstname",
            new_name="employee",
        ),
        migrations.RemoveField(
            model_name="save",
            name="employee_id",
        ),
        migrations.RemoveField(
            model_name="save",
            name="employee_lastname",
        ),
    ]
