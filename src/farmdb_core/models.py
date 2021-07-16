from django.db import models
from django.contrib.gis.db import models as gismodels
from django.contrib.postgres.fields import ArrayField
from address.models import AddressField


class SurveyAnswers(models.Model):
    # Many of: convetional, organic EU, organic demeter, transitioning, regen, market gardening, vegan, other
    farm_type = models.JSONField(null=True)
    # Many of: Agroforestry, Aquaculture, Beekeeping, etc
    production_methods = models.JSONField(null=True)
    # Many of: Meat, Fruits, Herbs, etc
    main_products = models.JSONField(null=True)  
    # Many of Sandy, Silty, etc.
    soil = models.JSONField(null=True)  
    # one of conventional, reduced, vertical, no-till
    tillage = models.JSONField(null=True)  
    # many of: synthetic, organinc, cover crops, no other
    fertilization = models.JSONField(null=True)
    irrigation = models.JSONField(null=True)  # Many of: Surface, floos, sprinkler, etc.
    # Yes or No to Pesticides, Herbicides, Fungicides, etc.
    uses_icides = models.BooleanField(null=True)
    receives_funding = models.BooleanField(null=True)  # Yes or No
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['created']

    def __str__(self) -> str:
        return f"{self.created}"


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
    description = models.TextField(max_length=2048, null=True)
    website = models.URLField(null=True)
    address = AddressField(on_delete=models.CASCADE, null=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['created']


class Farm(Organization):
    # Farm specific information:
    farm_size_approx = models.IntegerField(null=True)
    date_joined = models.DateField(auto_now_add=True)
    public_profile = models.BooleanField(default=False)
    # Relations:
    survey_answers = models.OneToOneField(
        SurveyAnswers,
        on_delete=models.CASCADE,
        null=True
    )
    organization = models.OneToOneField(
        to=Organization, 
        parent_link=True, 
        on_delete=models.CASCADE
    )

    def __str__(self):
        return f"{self.name}"


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
    )  # One of: phone, email, whatsapp, other

    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['created']

    def __str__(self) -> str:
        return f"{self.last_name}, {self.first_name}"


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

    def __str__(self) -> str:
        return f"{self.field_name}"

class Crop(models.Model):
    pass


class Practice(models.Model):
    pass
