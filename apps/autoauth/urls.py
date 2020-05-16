__author__ = "ハリネズミ"

from django.urls import path
from . import views

app_name = "autoauth"

urlpatterns = [
    path('login', views.LoginView.as_view(), name="login"),
]

