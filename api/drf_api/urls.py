"""drf_api URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView
from .views import logout_route
from users.views import landing_page, register, login, welcome_auth

urlpatterns = [
    path('', landing_page, name='landing-page'),
    path('auth/register/', register, name='register'),
    path('auth/login/', login, name='login'),
    path('auth/welcome/', welcome_auth, name='welcome-auth'),
    path('admin/', admin.site.urls),
    path('api/api-auth/', include('rest_framework.urls')),
    # our logout route has to be above the default one to be matched first
    path('api/dj-rest-auth/logout/', logout_route),
    path('api/dj-rest-auth/', include('dj_rest_auth.urls')),
    path(
        'api/dj-rest-auth/registration/', include('dj_rest_auth.registration.urls')
    ),
    path('api/', include('users.urls')),
    path('api/', include('posts.urls')),
    path('api/', include('comments.urls')),
    path('api/', include('likes.urls')),
    path('api/', include('followers.urls')),
    path('api/', include('messaging.urls')),
]

handler404 = TemplateView.as_view(template_name='index.html')