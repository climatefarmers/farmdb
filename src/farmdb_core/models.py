from django.db import models
from django.contrib.gis.db import models as gismodels
from django.contrib.postgres.fields import ArrayField
from address.models import AddressField


class SurveyAnswers(models.Model):
    farm_type = models.JSONField() # Many of: convetional, organic EU, organic demeter, transitioning, regen, market gardening, vegan, other
    production_methods = models.JSONField() # Many of: Agroforestry, Aquaculture, Beekeeping, etc
    main_products = models.JSONField() # Many of: Meat, Fruits, Herbs, etc
    soil = models.JSONField() # Many of Sandy, Silty, etc.
    tillage = models.JSONField() # one of conventional, reduced, vertical, no-till
    fertilization = models.JSONField() # many of: synthetic, organinc, cover crops, no other
    irrigation = models.JSONField() # Many of: Surface, floos, sprinkler, etc.
    uses_icides = models.BooleanField(null=True) # Yes or No to Pesticides, Herbicides, Fungicides, etc.
    receives_funding = models.BooleanField(null=True) # Yes or No
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['created']

class ProfileMedia(models.Model):
    # pictures =
    # video =
    pass


class CommunicationPreferences(models.Model):
    class CommunicationChoices(models.IntegerChoices):
        PHONE = 1
        EMAIL = 2
        WHATSAPP = 3
        # TODO: Handle other
    comm_channel = models.IntegerField(choices=CommunicationChoices.choices)


class Organization(models.Model):
    name = models.CharField(max_length=64)
    description = models.TextField(max_length=2048)
    website = models.URLField()
    address = AddressField(on_delete=models.CASCADE, null=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['created']


class Farm(Organization):
    # Farm specific information: 
    farm_size_approx = models.IntegerField()
    date_joined = models.DateField(auto_now_add=True)
    public_profile = models.BooleanField(default=False)
    # Relations: 
    survey_answers = models.OneToOneField(
        SurveyAnswers,
        on_delete=models.CASCADE,
        )


class Consultancy(Organization):
    pass

class Role(models.Model):
    class RoleChoices(models.IntegerChoices):
        FARMER = 1
        CONSULTANT = 2
        # TODO: Handle other
    role = models.IntegerField(choices=RoleChoices.choices)

class Person(models.Model):
    # Basic information
    first_name = models.CharField(max_length=32)
    last_name = models.CharField(max_length=32)
    email = models.EmailField(max_length=128)
    phone = models.CharField(max_length=16)
    # Relations:
    address = AddressField(on_delete=models.CASCADE, null=True)
    comm_pref = models.ForeignKey(
        CommunicationPreferences,
        on_delete=models.PROTECT,
        ) # One of: phone, email, whatsapp, other

    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['created']

class PersonToRoleToOrg(models.Model):
    person = models.ForeignKey(
        Person,
        on_delete=models.PROTECT
        )
    role = models.ForeignKey(
        Role,
        on_delete=models.PROTECT
        ) 
    organization = models.ForeignKey(
        Organization,
        on_delete=models.PROTECT
        )

class Field(models.Model):
    field_name = models.CharField(max_length=32)
    geom = gismodels.PolygonField(srid=4326)
    farm = models.ForeignKey('Farm', on_delete=models.PROTECT)


class Crop(models.Model):
    pass


class Practice(models.Model):
    pass
