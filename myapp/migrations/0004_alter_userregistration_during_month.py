# Generated by Django 5.1 on 2025-01-06 11:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0003_alter_userregistration_during_month'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userregistration',
            name='during_month',
            field=models.IntegerField(max_length=2),
        ),
    ]
