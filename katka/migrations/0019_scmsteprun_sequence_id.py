# Generated by Django 2.1.5 on 2019-05-07 01:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('katka', '0018_auto_20190506_0425'),
    ]

    operations = [
        migrations.AddField(
            model_name='scmsteprun',
            name='sequence_id',
            field=models.CharField(blank=True, max_length=30, null=True),
        ),
    ]
