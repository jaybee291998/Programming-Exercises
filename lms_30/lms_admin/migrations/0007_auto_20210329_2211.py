# Generated by Django 3.1.4 on 2021-03-29 14:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lms_admin', '0006_admin_model_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='admin',
            name='model_name',
            field=models.CharField(default='default mode name', max_length=255),
        ),
    ]
