# Generated by Django 2.0.1 on 2018-01-28 18:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sde', '0003_crate_table_index_solarsystem'),
    ]

    operations = [
        migrations.CreateModel(
            name='SolarSystemJump',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
            options={
                'db_table': 'mapSolarSystemJumps',
                'managed': False,
            },
        ),
    ]
