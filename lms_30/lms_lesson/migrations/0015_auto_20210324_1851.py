# Generated by Django 3.1.4 on 2021-03-24 10:51

from django.db import migrations
import lms_lesson.models


class Migration(migrations.Migration):

    dependencies = [
        ('lms_lesson', '0014_auto_20210324_1850'),
    ]

    operations = [
        migrations.AlterField(
            model_name='lecturefile',
            name='file',
            field=lms_lesson.models.CustomFileField(upload_to=''),
        ),
    ]
