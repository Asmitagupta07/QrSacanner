# Generated by Django 5.1 on 2025-01-06 11:50

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0004_alter_userregistration_during_month'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userregistration',
            name='during_month',
            field=models.PositiveSmallIntegerField(help_text='Enter a valid month (1-12).', validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(12)]),
        ),
    ]
