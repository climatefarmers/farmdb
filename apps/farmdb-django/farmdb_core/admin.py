from django.contrib import admin
from django.contrib.gis import admin as gisadmin
from .models import Field, Farm, SurveyAnswers, Person
@admin.register(Field)
class FieldAdmin(gisadmin.OSMGeoAdmin):
    fields = ['field_name','geom', 'farm']
    map_info = True

    layers = (
        ('maps', 1),
        ('photos', 0.3),
    )

admin.site.register(Farm, admin.ModelAdmin)
admin.site.register(SurveyAnswers, admin.ModelAdmin)
admin.site.register(Person, admin.ModelAdmin)