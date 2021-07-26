from django.urls import path
from . import views

urlpatterns = [
    path('farmsurveyresponse/', views.TypeFormFarmerSurvey.as_view()),
    path('', views.index, name="home"),
    path('map/', views.FieldsMapView.as_view()),
    path('farms/', views.FarmsView.as_view(), name="farms"),
    path('farms/<int:pk>/', views.FarmDetail.as_view(), name='farm_detail'),
    path('field/<int:pk>/', views.FieldDetail.as_view(), name='field_detail'),
]
