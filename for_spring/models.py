from django.db import models


# Create your models here.
class Test(models.Model):
    version = models.CharField(primary_key=True, max_length=10)
    # title = models.CharField(max_length=200)
    # text = models.TextField()
    # image = models.ImageField(default='default_image.jpeg')
    csv = models.CharField(max_length=200, default='http://220.66.115.158:8000/media/Anomaly_Simulation_with_tzinfo_v0.csv')
