# Generated by Django 2.1.5 on 2019-05-01 09:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("katka", "0016_auto_20190425_0922"),
    ]

    operations = [
        migrations.AlterField(
            model_name="scmpipelinerun", name="pipeline_yaml", field=models.TextField(default="---"),
        ),
        migrations.AlterField(
            model_name="scmpipelinerun", name="steps_total", field=models.PositiveSmallIntegerField(default=0),
        ),
    ]
