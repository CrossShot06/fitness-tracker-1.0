from django.contrib import admin
from django.urls import path
from . import views
from .admin_site import custom_admin_site

urlpatterns = [
    path('', views.home,name="home"),
    path('user/',views.user,name="user"),
    path('trainer/',views.trainer,name="trainer"),
    path('register/',views.register,name="register"),
    path('login/',views.login_view,name="login"),
    path('logout/',views.logout_view,name='logout'),
    path('trainer_request/',views.trainer_request,name='trainer_request')
]
