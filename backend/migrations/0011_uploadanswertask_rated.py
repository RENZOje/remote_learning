# Generated by Django 3.1.7 on 2021-03-25 11:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0010_auto_20210325_1343'),
    ]

    operations = [
        migrations.AddField(
            model_name='uploadanswertask',
            name='rated',
            field=models.BooleanField(default=False),
        ),
    ]