# Generated by Django 2.0.1 on 2018-01-17 09:01

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ('sde', '0002_jump'),
    ]

    operations = [
        migrations.RunSQL(
            'CREATE INDEX "ix_mapSolarSystems_solarSystemName" on "mapSolarSystems" (upper("solarSystemName"))')
    ]
