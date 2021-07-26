from django.urls import path, include
from rest_framework import routers
from . import views

router = routers.DefaultRouter()
router.register(r'farms', views.FarmsViewSet)

urlpatterns = [
    path('farmsurveyresponse/', views.TypeFormFarmerSurvey.as_view()),
    path('', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
]
