# Generated by Django 3.2.13 on 2022-06-19 09:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('for_spring', '0002_alter_test_csv'),
    ]

    operations = [
        migrations.AlterField(
            model_name='test',
            name='csv',
            field=models.CharField(default='http://220.66.115.158:8000/media/Anomaly_Simulation_with_tzinfo_v0.csv', max_length=200),
        ),
    ]