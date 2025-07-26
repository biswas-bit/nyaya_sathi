from django.urls import path
from . import views

app_name = 'guide'

urlpatterns = [
    path("", views.home,name="guide_home"),
    path("chat/",views.chat,name="chat")
    
]
