# Generated by Django 3.1.4 on 2021-03-11 01:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lms_studentwork', '0003_auto_20210310_1457'),
    ]

    operations = [
        migrations.AddField(
            model_name='studentwork',
            name='remark',
            field=models.TextField(default='Good Job :)'),
            preserve_default=False,
        ),
    ]
