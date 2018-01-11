# Generated by Django 2.0.1 on 2018-01-09 14:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0005_celestial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='celestial',
            name='constellationID',
            field=models.IntegerField(db_index=True),
        ),
        migrations.AlterField(
            model_name='celestial',
            name='regionID',
            field=models.IntegerField(db_index=True),
        ),
        migrations.AlterField(
            model_name='celestial',
            name='solarSystemID',
            field=models.IntegerField(db_index=True),
        ),
        migrations.AlterField(
            model_name='celestial',
            name='typeID',
            field=models.IntegerField(db_index=True),
        ),
    ]
