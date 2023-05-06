from django.urls import path
from . import views

urlpatterns = [
    path("", views.init, name="init"),
    path("", views.chat, name="chat"),
]
