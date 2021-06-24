from django.db import models
from django.contrib.gis.db import models as gismodels
from django.db.models.deletion import PROTECT
from address.models import AddressField

# Create your models here.
class Farm(models.Model):
    farm_name = models.CharField(max_length=64)
    farm_address = AddressField(on_delete=models.CASCADE)
    description = models.TextField(max_length=2048)

class Person(models.Model):
    first_name = models.CharField(max_length=32)
    last_name = models.CharField(max_length=32)
    email = models.EmailField(max_length=128)
    # TODO: telephone w. sms validation
    address = AddressField(on_delete=models.CASCADE)

class Field(models.Model):
    field_name = models.CharField(max_length=32)
    geom = gismodels.PolygonField(srid=4326)
    farm = models.ForeignKey('Farm', on_delete=models.PROTECT)

class Crop(models.Model):
    pass

class Practice(models.Model):
    pass

