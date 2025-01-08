# Generated by Django 5.1 on 2025-01-08 10:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0006_userregistration_make'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userregistration',
            name='Make',
            field=models.CharField(blank=True, choices=[('DPSU', 'make in india(dpsu)'), ('PSU', 'make in india(psu)'), ('STARTUP', 'make in india(startup)'), ('RAKSHA RATNAM', 'make in india(raksha ratnam)'), ('PRIVATE', 'make in india(private)'), ('DBT', 'make in india(dbt)'), ('LC', 'foreign procurement(lc)')], max_length=30, null=True),
        ),
    ]