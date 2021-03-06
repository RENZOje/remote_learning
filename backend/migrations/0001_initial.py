# Generated by Django 3.1.7 on 2021-03-07 17:28

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Course',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(blank=True, max_length=250)),
                ('description', models.TextField(blank=True)),
                ('link', models.SlugField()),
            ],
        ),
        migrations.CreateModel(
            name='Group_custom',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=10)),
                ('link', models.SlugField()),
            ],
        ),
        migrations.CreateModel(
            name='Teacher',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('firstName', models.CharField(blank=True, max_length=50)),
                ('lastName', models.CharField(blank=True, max_length=50)),
                ('middleName', models.CharField(blank=True, max_length=50)),
                ('email', models.EmailField(blank=True, max_length=50)),
                ('phone', models.CharField(blank=True, max_length=50)),
                ('link', models.SlugField()),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Student',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('firstName', models.CharField(blank=True, max_length=50)),
                ('lastName', models.CharField(blank=True, max_length=50)),
                ('middleName', models.CharField(blank=True, max_length=50)),
                ('email', models.EmailField(blank=True, max_length=50)),
                ('phone', models.CharField(blank=True, max_length=50)),
                ('link', models.SlugField()),
                ('group', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='backend.group_custom')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Section',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(blank=True, max_length=250)),
                ('description', models.TextField(blank=True)),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='backend.course')),
            ],
        ),
        migrations.CreateModel(
            name='Quiz',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(blank=True, max_length=250)),
                ('createdAt', models.DateTimeField(auto_now_add=True)),
                ('point', models.IntegerField(blank=True)),
                ('section', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='backend.section')),
            ],
        ),
        migrations.AddField(
            model_name='course',
            name='students',
            field=models.ManyToManyField(blank=True, to='backend.Student'),
        ),
        migrations.AddField(
            model_name='course',
            name='teachers',
            field=models.ManyToManyField(blank=True, to='backend.Teacher'),
        ),
        migrations.CreateModel(
            name='Article',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(blank=True, max_length=250)),
                ('createdAt', models.DateTimeField(auto_now_add=True)),
                ('section', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='backend.section')),
            ],
        ),
    ]
