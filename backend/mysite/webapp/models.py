from django.db import models

# Create your models here.
class Floorplan(models.Model):
    title = models.TextField(unique=True)
    plan = models.ImageField()
    aplist = models.TextField(null=True)
    status = models.TextField(default="NEW")

    def __str__(self):
        return self.title

class MappedPoint(models.Model):
    imgcoordinate = models.TextField()
    scanvalues = models.TextField()
    plan = models.TextField(null=True)

    def __str__(self):
        return self.imgcoordinate