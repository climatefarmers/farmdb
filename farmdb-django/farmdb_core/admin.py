from django.contrib import admin
from django.contrib.gis import admin as gisadmin
from .models import Field, Farm, SurveyAnswers, Person
# Register your models here.

#class FieldAdmin(admin.ModelAdmin):
#    fields = ['field_name','geom']

admin.site.register(Field, gisadmin.OSMGeoAdmin)
admin.site.register(Farm, admin.ModelAdmin)
admin.site.register(SurveyAnswers, admin.ModelAdmin)
admin.site.register(Person, admin.ModelAdmin)