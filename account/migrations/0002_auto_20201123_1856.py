# Generated by Django 3.1.3 on 2020-11-23 17:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main_system', '0004_auto_20201120_1129'),
        ('account', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='caterings',
            field=models.ManyToManyField(blank=True, to='main_system.Catering'),
        ),
        migrations.AlterField(
            model_name='profile',
            name='locals',
            field=models.ManyToManyField(blank=True, to='main_system.Room'),
        ),
        migrations.AlterField(
            model_name='profile',
            name='other_offers',
            field=models.ManyToManyField(blank=True, to='main_system.OtherOffer'),
        ),
    ]
