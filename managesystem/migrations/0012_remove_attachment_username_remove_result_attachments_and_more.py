# Generated by Django 4.2.6 on 2023-10-24 17:54

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("managesystem", "0011_attachment_username"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="attachment",
            name="username",
        ),
        migrations.RemoveField(
            model_name="result",
            name="attachments",
        ),
        migrations.AddField(
            model_name="attachment",
            name="result",
            field=models.ForeignKey(
                default=1,
                on_delete=django.db.models.deletion.CASCADE,
                to="managesystem.result",
            ),
            preserve_default=False,
        ),
        migrations.CreateModel(
            name="savefile",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("attachments", models.ManyToManyField(to="managesystem.attachment")),
            ],
        ),
    ]
