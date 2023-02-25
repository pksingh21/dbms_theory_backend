# Generated by Django 4.1.7 on 2023-02-25 17:09

import django.contrib.postgres.fields
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("apis", "0009_alter_setofattributes_attributes"),
    ]

    operations = [
        migrations.AddField(
            model_name="setofattributes",
            name="ok",
            field=django.contrib.postgres.fields.ArrayField(
                base_field=models.CharField(max_length=2),
                default=list,
                max_length=20,
                size=None,
            ),
        ),
    ]
