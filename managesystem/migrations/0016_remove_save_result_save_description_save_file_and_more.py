# Generated by Django 4.2.7 on 2023-11-20 21:59

from django.db import migrations, models
import managesystem.models


class Migration(migrations.Migration):

    dependencies = [
        ("managesystem", "0015_rename_result_save_result"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="save",
            name="result",
        ),
        migrations.AddField(
            model_name="save",
            name="description",
            field=models.CharField(default=1, max_length=255),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="save",
            name="file",
            field=models.FileField(
                blank=True, null=True, upload_to=managesystem.models.user_directory_path
            ),
        ),
        migrations.AddField(
            model_name="save",
            name="score",
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AddField(
            model_name="save",
            name="total",
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AddField(
            model_name="save",
            name="unit",
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AddField(
            model_name="save",
            name="work",
            field=models.CharField(default=1, max_length=255),
            preserve_default=False,
        ),
    ]
