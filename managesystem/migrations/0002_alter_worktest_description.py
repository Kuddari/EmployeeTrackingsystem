# Generated by Django 4.2.6 on 2023-11-07 13:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("managesystem", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="worktest",
            name="description",
            field=models.TextField(),
        ),
    ]