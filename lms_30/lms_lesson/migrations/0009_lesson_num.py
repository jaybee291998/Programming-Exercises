# Generated by Django 3.1.4 on 2021-03-16 02:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lms_lesson', '0008_lecture'),
    ]

    operations = [
        migrations.AddField(
            model_name='lesson',
            name='num',
            field=models.IntegerField(default=0),
        ),
    ]
