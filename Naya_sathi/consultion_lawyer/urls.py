from django.urls import path
from . import views

app_name = "consultion_lawyer"
urlpatterns = [
    path('', views.consult, name='consult'),
]
