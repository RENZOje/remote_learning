# Generated by Django 3.1.7 on 2021-03-25 14:20

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0012_auto_20210325_1500'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='UploadTask',
            new_name='Assignment',
        ),
        migrations.RenameModel(
            old_name='ResultUploadAnswerTask',
            new_name='ResultAssignment',
        ),
        migrations.RenameModel(
            old_name='UploadAnswerTask',
            new_name='UploadAssignment',
        ),
    ]
