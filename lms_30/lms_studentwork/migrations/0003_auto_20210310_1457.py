# Generated by Django 3.1.4 on 2021-03-10 06:57

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('lms_studentwork', '0002_auto_20210310_1426'),
    ]

    operations = [
        migrations.AlterField(
            model_name='studentworkcomment',
            name='author',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='studentworkcomment', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='studentworkcomment',
            name='content',
            field=models.TextField(),
        ),
    ]
