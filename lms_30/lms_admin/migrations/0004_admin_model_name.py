# Generated by Django 3.1.4 on 2021-03-29 14:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lms_admin', '0003_auto_20210329_2147'),
    ]

    operations = [
        migrations.AddField(
            model_name='admin',
            name='model_name',
            field=models.CharField(default='announcement', max_length=255),
            preserve_default=False,
        ),
    ]