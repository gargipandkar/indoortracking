from django.db import models

# Create your models here.
class Floorplan(models.Model):
    title = models.TextField()
    plan = models.ImageField()

    def __str__(self):
        return self.title

class MappedPoint(models.Model):
    imgcoordinate = models.TextField()
    scanvalues = models.TextField()

    def __str__(self):
        return self.imgcoordinate