# Generated by Django 3.1.7 on 2021-03-17 19:03

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0011_answer_question_quiz_result'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='quiz',
            name='topic',
        ),
    ]