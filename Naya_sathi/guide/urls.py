from django.urls import path
from . import views

app_name = 'guide'

urlpatterns = [
    path("", views.guidence,name="Guide")
]