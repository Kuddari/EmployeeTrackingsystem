# Generated by Django 4.2.6 on 2023-10-24 16:19

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("managesystem", "0001_initial"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="employee",
            name="firstname",
        ),
        migrations.RemoveField(
            model_name="employee",
            name="lastname",
        ),
        migrations.AlterField(
            model_name="employee",
            name="username",
            field=models.OneToOneField(
                on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL
            ),
        ),
    ]
