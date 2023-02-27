# Generated by Django 4.1.7 on 2023-02-27 09:59

import django.contrib.postgres.fields
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("apis", "0016_remove_setofattributes_functionaldependency_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="setofattributes",
            name="attributes",
            field=django.contrib.postgres.fields.ArrayField(
                base_field=models.CharField(max_length=1000000),
                default=list,
                max_length=20,
                size=None,
            ),
        ),
    ]
