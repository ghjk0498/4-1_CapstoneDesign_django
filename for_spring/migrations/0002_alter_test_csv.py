# Generated by Django 3.2.13 on 2022-06-19 09:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('for_spring', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='test',
            name='csv',
            field=models.CharField(default='http://220.66.115.158:8000/media/Anomaly Simulation with tzinfo v0.csv', max_length=200),
        ),
    ]