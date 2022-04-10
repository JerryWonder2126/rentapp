from django.urls import path
from . import views

urlpatterns = [
    path('', views.HomeView.as_view(), name='index'),
    path('products/', views.products_page, name='products_all'),
    path('products/<str:group>/', views.products_page, name='products_group'),
    path('products/<str:group>/<str:identifier>/', views.house_page, name='single_product'),
    path('products/offers/<str:group>/<str:filterby>/<str:filter>/', views.offers, name='offers_list'),
]
