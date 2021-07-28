from django.urls import path, include
from django.views.generic.base import TemplateView
from rest_framework import routers
from . import views

router = routers.DefaultRouter()
router.register(r'farms', views.FarmsViewSet)

urlpatterns = [
    path('farmsurveyresponse/', views.TypeFormFarmerSurvey.as_view()),
    path('', TemplateView.as_view(template_name='home.html'), name="home"),
    path('api/', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('farms/', views.FarmsView.as_view(), name="farms"),
    path('farms/<int:pk>/', views.FarmDetail.as_view(), name='farm_detail'),
    path('field/<int:pk>/', views.FieldDetail.as_view(), name='field_detail'),
]
