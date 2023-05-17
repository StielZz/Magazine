from django.urls import path
from django.conf import settings
from django.contrib.auth import views as auth_views
from django.conf.urls.static import static
from . import views

urlpatterns = [
    path('', views.index),

    path('catalog/', views.catalog, name='catalog'),
    path('catalog/pc', views.catalog_pc, name='catalog'),
    path('catalog/laptop', views.catalog_laptop, name='catalog'),
    path('catalog/search', views.search_product, name='search_product'),
    path('catalog/product_detail/<int:product_id>/', views.product_detail, name='product_detail'),
    path('catalog/product_detail/add_to_card/<int:product_id>/', views.add_to_cart, name='add_to_cart'),

    path('account/', views.account, name='account'),
    path('account/login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('account/logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('account/place-order/', views.place_order, name='place_order'),
    path('account/remove_from_cart/<int:product_id>/', views.remove_from_cart, name='remove_from_cart'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
