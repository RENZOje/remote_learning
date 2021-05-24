# Generated by Django 3.1.7 on 2021-05-24 18:18

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0017_auto_20210524_2030'),
    ]

    operations = [
        migrations.AddField(
            model_name='student',
            name='profilePicture',
            field=models.ImageField(blank=True, null=True, upload_to=''),
        ),
        migrations.AddField(
            model_name='teacher',
            name='about',
            field=models.CharField(blank=True, max_length=250),
        ),
        migrations.AddField(
            model_name='teacher',
            name='group',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='backend.group_custom'),
        ),
        migrations.AddField(
            model_name='teacher',
            name='profilePicture',
            field=models.ImageField(blank=True, null=True, upload_to=''),
        ),
        migrations.AddField(
            model_name='teacher',
            name='telegram_link',
            field=models.CharField(blank=True, max_length=100),
        ),
        migrations.AlterField(
            model_name='course',
            name='title',
            field=models.CharField(max_length=250),
        ),
    ]
