from django.db import models


# Create your models here.
class Test(models.Model):
    version = models.CharField(primary_key=True, max_length=10)
    # title = models.CharField(max_length=200)
    # text = models.TextField()
    # image = models.ImageField(default='default_image.jpeg')
    csv = models.FileField(default='Anomaly Simulation with tzinfo v0.csv')
