from django.db import models

# Create your models here.
class Test(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=200)
    text = models.TextField()
    image = models.ImageField(default='default_image.jpeg')