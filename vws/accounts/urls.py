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


    
    path('listvendors/', views.listvendors_view, name='listvendors_view'),
    path('api/login/', views.login_api, name='login_api'),
    path('api/getfeedback/', views.get_feedback_messages, name='get_feedback_messages'),
    path('api/createproduct/', views.craeteProduct_api, name='craeteProduct_api'),
    path('api/products/', views.get_products, name='get_products'),


]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
