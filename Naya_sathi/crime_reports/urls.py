from django.urls import path
from . import views

urlpatterns = [
    path('', views.crime_reports, name='crime_report'),
]