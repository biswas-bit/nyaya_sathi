from django.urls import path
from . import views

app_name = 'fir'

urlpatterns = [
    path('', views.report_fir, name='report_fir'),
    path('list/', views.fir_list, name='fir_list'),
]