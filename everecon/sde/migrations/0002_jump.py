# Generated by Django 2.0.1 on 2018-01-15 21:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sde', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Jump',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
            options={
                'db_table': 'mapJumps',
                'managed': False,
            },
        ),
    ]