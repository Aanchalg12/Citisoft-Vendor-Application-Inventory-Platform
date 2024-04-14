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
from .views import deleteuser
from .views import application_details
from .views import update_application
from .views import delete_application
# from .views import search_application
from .views import generate_report
from .views import search_results

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('accounts/login/', user_login, name='login'),
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
    path("saveupdateuser", views.saveupdateuser, name="saveupdateuser"),
    path('application/', views.application, name='application'),
    path("addapplication", views.addapplication, name="addapplication"),
    path('viewprofile/<int:user_id>/', views.viewprofile, name='viewprofile'),
    # path('search/', views.search_users, name='search_users'),
    path('search/', search_results, name='search_results'),
    path('<int:pk>', application_details, name='application_details'),
    path('<int:pk>/update/', update_application, name='update_application'),
    path('<int:pk>/delete/', delete_application, name='delete_application'),
    # path('search/', search_application, name='search_application'),
    path('generate-report/<int:application_id>/', generate_report, name='generate_report'),
    path('add-vendor/', views.vendor_details_add, name='vendor_details_add'),
    path('vendor_details', views.vendor_details, name="vendor_details"),
    path('vendor/<int:vendor_id>/', views.vendor_detail_info, name='vendor_detail_info'),
    path('vendor_info/<int:vendor_info_id>/pdf/', views.generate_vendor_info_pdf, name='vendor_info_pdf'),
    path('vendor_info/<int:vendor_info_id>/update/', views.update_vendor_info, name='update_vendor_info'),
    path('vendor_info/<int:vendor_info_id>/delete/', views.delete_vendor_info, name='delete_vendor_info'),
    path('deleteuser/<int:user_id>/', views.deleteuser, name='deleteuser'),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
