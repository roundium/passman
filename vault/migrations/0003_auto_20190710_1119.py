# Generated by Django 2.2.3 on 2019-07-10 11:19

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vault', '0002_auto_20190706_1245'),
    ]

    operations = [
        migrations.AlterField(
            model_name='credential',
            name='password',
            field=models.CharField(max_length=254, validators=[django.core.validators.MaxLengthValidator(64)], verbose_name='password'),
        ),
    ]