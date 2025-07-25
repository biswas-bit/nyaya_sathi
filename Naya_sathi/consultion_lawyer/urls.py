from django.urls import path
from . import views

urlpatterns = [
    path('', views.consult, name='consult'),
]
