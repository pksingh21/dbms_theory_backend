# Generated by Django 4.1.7 on 2023-02-25 17:16

import django.contrib.postgres.fields
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("apis", "0010_setofattributes_ok"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="setofattributes",
            name="ok",
        ),
        migrations.AlterField(
            model_name="setofattributes",
            name="attributes",
            field=django.contrib.postgres.fields.ArrayField(
                base_field=models.CharField(max_length=12),
                default=list,
                max_length=20,
                size=None,
            ),
        ),
    ]
