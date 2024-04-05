"""
URL configuration for myCitisoft project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
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
from django.urls import path
from django.contrib.auth.views import LoginView
from myCitisoft.views import signup, user_login
from . import views
from .views import logout_view
from .views import customerdashboard
from django.conf import settings
from django.conf.urls.static import static
# from .views import soft_delete_user

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', user_login, name='login'),
    path('signup/', signup, name='signup'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path("admindashboard", views.admindashboard, name="admindashboard"), 
    path("reviewerdashboard", views.reviewerdashboard, name="reviewerdashboard"), 
    path("vendordashboard", views.vendordashboard, name="vendordashboard"), 
    path("customerdashboard", customerdashboard, name="customerdashboard"), 
    path("userprofile", views.userprofile, name="userprofile"),
    path('logout/', logout_view, name='logout'),
    path('user_list/', views.user_list, name='user_list'),
    path("adduser", views.adduser, name="adduser"),
    path("saveadduser", views.saveadduser, name="saveadduser"),
    path("deleteuser", views.deleteuser, name="deleteuser"),
    path("saveupdateuser", views.saveupdateuser, name="saveupdateuser"),
    path('application/', views.application, name='application'),
    path('viewprofile/<int:user_id>/', views.viewprofile, name='viewprofile'),
    path('search/', views.search_users, name='search_users'),
    # path('soft-delete/<int:user_id>/', soft_delete_user, name='soft_delete_user'),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)