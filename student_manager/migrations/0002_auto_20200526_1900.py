# Generated by Django 2.2.12 on 2020-05-26 19:00

from django.db import migrations, models
import djongo.models.fields
import student_manager.models


class Migration(migrations.Migration):

    dependencies = [
        ('student_manager', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='MicroContentProgress',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('micro_content_id', models.IntegerField()),
                ('name', models.CharField(max_length=100)),
                ('completed', models.BooleanField(default=False)),
                ('mark', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='UnitProgress',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('completed', models.BooleanField(default=False)),
                ('next_micro_content_id', models.IntegerField()),
                ('micro_contents', djongo.models.fields.ArrayModelField(model_container=student_manager.models.MicroContentProgress)),
            ],
        ),
        migrations.AddField(
            model_name='student',
            name='progress',
            field=djongo.models.fields.ArrayModelField(default='-', model_container=student_manager.models.UnitProgress),
        ),
    ]