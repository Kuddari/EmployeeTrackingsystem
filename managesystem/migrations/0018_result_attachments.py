# Generated by Django 4.2.6 on 2023-10-24 18:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("managesystem", "0017_rename_file_savedata_attachments"),
    ]

    operations = [
        migrations.AddField(
            model_name="result",
            name="attachments",
            field=models.ManyToManyField(to="managesystem.attachment"),
        ),
    ]
