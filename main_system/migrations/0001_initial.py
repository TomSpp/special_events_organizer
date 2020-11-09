# Generated by Django 3.1.3 on 2020-11-09 17:47

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Catering',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('with_local_only', models.BooleanField(default=False)),
                ('min_cost_per_person', models.DecimalField(decimal_places=2, max_digits=10)),
                ('basic_offer', models.CharField(max_length=1000, null=True)),
                ('added', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Contact',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('phone_number', models.CharField(max_length=20)),
                ('website', models.URLField(max_length=100, null=True)),
                ('email', models.EmailField(max_length=100, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Local',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('added', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('catering', models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to='main_system.catering')),
                ('contact', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='main_system.contact')),
            ],
        ),
        migrations.CreateModel(
            name='Location',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('voivodeship', models.CharField(max_length=100)),
                ('district', models.CharField(max_length=100)),
                ('town', models.CharField(max_length=100)),
                ('street', models.CharField(max_length=100)),
                ('local_number', models.CharField(max_length=10)),
            ],
        ),
        migrations.CreateModel(
            name='Room',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('max_people', models.IntegerField()),
                ('cost', models.DecimalField(decimal_places=2, max_digits=10)),
                ('type_of_parquet', models.CharField(max_length=100, null=True)),
                ('air_conditioned', models.BooleanField(null=True)),
                ('local', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main_system.local')),
            ],
        ),
        migrations.CreateModel(
            name='OtherOffer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('min_cost', models.DecimalField(decimal_places=2, max_digits=10)),
                ('basic_offer', models.CharField(max_length=1000, null=True)),
                ('added', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('contact', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='main_system.contact')),
                ('location', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='main_system.location')),
            ],
        ),
        migrations.AddField(
            model_name='local',
            name='location',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='main_system.location'),
        ),
        migrations.AddField(
            model_name='catering',
            name='contact',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='main_system.contact'),
        ),
        migrations.AddField(
            model_name='catering',
            name='location',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='main_system.location'),
        ),
    ]
