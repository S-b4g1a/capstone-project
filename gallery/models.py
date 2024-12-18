from django.db import models

# Create your models here.

class Gallery(models.Model):
    hotel =  models.ForeignKey(Hotel, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='gallery/')
    caption = models.CharField(max_length=100, blank=True)