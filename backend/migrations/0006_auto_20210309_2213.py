# Generated by Django 3.1.7 on 2021-03-09 20:13

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0005_auto_20210309_2159'),
    ]

    operations = [
        migrations.AlterField(
            model_name='student',
            name='group',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='backend.group_custom'),
        ),
    ]