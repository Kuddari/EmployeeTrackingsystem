# Generated by Django 4.2.6 on 2023-11-07 14:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        (
            "managesystem",
            "0005_result_setunit_work_remove_worktest_employeeposition_and_more",
        ),
    ]

    operations = [
        migrations.RemoveField(
            model_name="setunit",
            name="employeeposition",
        ),
        migrations.AddField(
            model_name="setunit",
            name="position",
            field=models.CharField(
                choices=[
                    ("Dean", "Dean"),
                    ("Lecturer", "Lecturer"),
                    ("Researcher", "Researcher"),
                ],
                default=1,
                max_length=50,
            ),
            preserve_default=False,
        ),
    ]