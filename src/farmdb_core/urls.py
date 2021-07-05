from django.urls import path
from .views import TypeFormFarmerSurvey

urlpatterns = [
    path('farmsurveyresponse/', TypeFormFarmerSurvey.as_view())
]