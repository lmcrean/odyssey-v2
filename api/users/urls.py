# users/urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('', views.landing_page, name='landing-page'),
    path('auth/register/', views.register, name='register'),
    path('auth/login/', views.login, name='login'),
    path('auth/welcome/', views.welcome_auth, name='welcome-auth'),
]
