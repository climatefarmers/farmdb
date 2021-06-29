from django.db import models
from django.contrib.gis.db import models as gismodels
from django.db.models.deletion import PROTECT
from address.models import AddressField

# Create your models here.
class Farm(models.Model):
    name = models.CharField(max_length=64)
    description = models.TextField(max_length=2048)
    #website = 
    #team_size =
    #farm_size_approx = 
    #main_products = 
    #date_joined = 
    #public_profile =
    #pictures =
    #video = 

    farm_address = AddressField(on_delete=models.CASCADE, null=True)

class Person(models.Model):
    first_name = models.CharField(max_length=32)
    last_name = models.CharField(max_length=32)
    email = models.EmailField(max_length=128)
    # TODO: telephone w. sms validation
    #telephone = 
    address = AddressField(on_delete=models.CASCADE, null=True)

class Field(models.Model):
    field_name = models.CharField(max_length=32)
    geom = gismodels.PolygonField(srid=4326)
    farm = models.ForeignKey('Farm', on_delete=models.PROTECT)

class Crop(models.Model):
    pass

class Practice(models.Model):
    pass

