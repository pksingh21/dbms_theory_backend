# Generated by Django 4.1.7 on 2023-02-25 18:04

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("apis", "0012_delete_geeksmodel"),
    ]

    operations = [
        migrations.AddField(
            model_name="setofattributes",
            name="FunctionalDependency",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to="apis.functionaldependency",
            ),
        ),
    ]
