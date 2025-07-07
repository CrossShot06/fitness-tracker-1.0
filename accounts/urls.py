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
    path('trainer_request/',views.trainer_request,name='trainer_request'),
    path('page-redirect/',views.page_redirect,name='page-redirect'),
    path('trainer_assign/',views.trainer_assign,name='trainer_assign'),
    path('inbox/',views.inbox,name='inbox'),
    path('reviews/<str:username>/',views.reviews_page,name='reviews_page'),
    path('my-reviews/', views.trainer_reviews_view, name='trainer_reviews'),
    path('dashboard/',views.dashboard,name='dashboard'),
    path('set_goals/', views.set_goals, name='set_goals')
]
