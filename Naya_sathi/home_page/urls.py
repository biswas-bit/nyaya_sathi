from django.urls import path
from . import views

app_name = 'home_page'

urlpatterns = [
    path('', views.index, name='index'),
    path('showcase/<int:step>/', views.showcase, name='showcase'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('features/', views.feature_selection, name='feature_selection'),
]