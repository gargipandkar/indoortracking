from django.contrib import admin

# Register your models here.
from .models import Floorplan, MappedPoint

admin.site.register(Floorplan)
admin.site.register(MappedPoint)
