from django.urls import path
from .views import signup
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('api/signup/', signup, name='signup'),
    path('', views.login_view, name='login_view'),
    path('login/', views.login_view, name='login_view'),
    path('signup/', views.signup_view, name='login_view'),
    path('viewproduct/', views.viewproduct_view, name='download-docx'),
    path('listselected/', views.listselectproducts_view, name='listselectproducts_view'),
    path('listclients/', views.listclients, name='listclients'),
    path('createproduct/', views.create_product_view, name='create_product_view'),
    path('vendorhome/', views.vendor_home_view, name='vendor_home_view'),
    path('viewprod/', views.viewproductvendor, name='viewproductvendor'),
    path('clienthome/', views.clienthome_view, name='clienthome_view'),
    path('listinterseted/', views.listinterseted_view, name='listinterseted_view'),
    path('api/feedback/', views.create_feedback, name='create_feedback'),
    path('profile/', views.profile_view, name='profile_view'),
        path('viewvendorprofile/', views.viewvendorprofile, name='viewvendorprofile'),
                path('viewclient/', views.view_client, name='view_client'),
                path('vendor_profile/', views.view_client, name='view_client'),


    
    path('listvendors/', views.listvendors_view, name='listvendors_view'),
    path('api/login/', views.login_api, name='login_api'),
    path('api/getfeedback/', views.get_feedback_messages, name='get_feedback_messages'),
    path('api/createproduct/', views.craeteProduct_api, name='craeteProduct_api'),
    path('api/products/', views.get_products, name='get_products'),
    path('api/products/<int:product_id>/', views.update_product, name='update_product'),
    path('api/updateproductinfo/<int:product_id>/', views.update_product_info, name='update_product_info'),
    path('download/<filename>', views.download_docx, name='download-docx'),
    path('api/user_list/', views.user_list, name='user_list'),
    path('api/users/<int:user_id>/', views.get_user_by_id, name='get-user-by-id'),
        path('api/get_all_user_profiles', views.get_all_user_profiles, name='get_all_user_profiles'),


]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
