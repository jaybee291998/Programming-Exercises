# Generated by Django 3.1.4 on 2021-03-07 01:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lms_class', '0003_remove_lmsclass_semester'),
    ]

    operations = [
        migrations.AddField(
            model_name='lmsclass',
            name='semester',
            field=models.CharField(choices=[('PRE', 'Prelim'), ('MID', 'Midterm')], default='PRE', max_length=3),
        ),
        migrations.AlterField(
            model_name='lmsclass',
            name='course',
            field=models.CharField(choices=[('CS', 'BSCS'), ('ED', 'BSED'), ('PS', 'BAPS')], default='CS', max_length=2),
        ),
        migrations.AlterField(
            model_name='lmsclass',
            name='year',
            field=models.CharField(choices=[('1', '1st'), ('2', '2nd'), ('3', '3rd'), ('4', '4th'), ('5', 'Grad')], default='1', max_length=1),
        ),
    ]