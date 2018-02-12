# Generated by Django 2.0.1 on 2018-01-28 21:04

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('sde', '0005_ship'),
        ('navigate', '0002_auto_20180128_1829'),
    ]

    operations = [
        migrations.AddField(
            model_name='kill',
            name='ship',
            field=models.ForeignKey(default=11200, on_delete=django.db.models.deletion.PROTECT, to='sde.Ship'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='kill',
            name='victim_alliance_id',
            field=models.IntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='kill',
            name='victim_corporation_id',
            field=models.IntegerField(null=True),
        ),
    ]