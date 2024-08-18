"""
URL configuration for MovieTicketing project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
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
from auths import views


from django.urls import  path


urlpatterns = [
    path('register/',views.register,name='register' ),
    path('login/',views.Login,name='login' ),
    path('logout/',views.Logout,name='logout' ),
     path('user_profile/', views.user_profile, name='user_profile'),
     path('change_password/', views.change_password, name='change_password'),
     path('profile/edit/', views.edit_profile, name='edit_profile'),
    
     


]
