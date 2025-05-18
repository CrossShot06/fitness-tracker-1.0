from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home,name="home"),
    path('user/',views.user,name="user"),
    path('trainer/',views.trainer,name="trainer"),
    path('register/',views.register,name="register"),
    path('login/',views.login_view,name="login"),
]
