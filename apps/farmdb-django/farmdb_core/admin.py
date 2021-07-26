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

    #def get_form(self, request, obj=None, **kwargs):
    #    """
    #    Use special form during foo creation
    #    """
    #    defaults = {}
    #    if obj is None:
    #        defaults['form'] = self.custom_form
    #    defaults.update(kwargs)
    #    print(defaults)
    #    return super().get_form(request, obj, **defaults)
    

admin.site.register(Farm, admin.ModelAdmin)
admin.site.register(SurveyAnswers, admin.ModelAdmin)
admin.site.register(Person, admin.ModelAdmin)