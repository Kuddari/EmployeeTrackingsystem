# Generated by Django 4.2.6 on 2023-11-08 13:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("managesystem", "0010_result_result_result_total"),
    ]

    operations = [
        migrations.AlterField(
            model_name="work",
            name="name",
            field=models.CharField(max_length=100),
        ),
    ]