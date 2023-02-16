"""mysite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
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
# mysite/urls.py

from django.contrib import admin
from django.urls import path
from SteamSimilar import views
from django.contrib.auth import views as auth_views
from SteamSimilar.forms import LoginForm, SignInForm

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='index'),
    path('topic/<int:topic_id>/', views.topic, name='topic'),
    path('new_post/', views.new_post, name='new_post'),
    path('new_comment/', views.new_comment, name='new_comment'),
    path('tags/', views.tags, name='tags'),
    path('aboutme/', views.aboutme, name='aboutme'),
    path('login/', auth_views.LoginView.as_view(template_name='registration/login.html', form_class=LoginForm), name='login'),
    path('signin/', auth_views.LoginView.as_view(template_name='registration/signin.html', authentication_form=SignInForm), name='signin'),
]
