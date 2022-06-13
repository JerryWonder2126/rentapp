from django.urls import path
from . import views

urlpatterns = [
    path('', views.HomeView.as_view(), name='index'),
    path('accounts/profile/', views.Dashboard.as_view(), name='profile'),
    path('accounts/staff/add', views.mark_as_staff, name='add staff'),
    path('faqs/', views.faqs, name='faqs'),
    path('products/', views.products_page, name='products_all'),
    path('products/<str:group>/', views.products_page, name='products_group'),
    path('products/<str:group>/<str:identifier>/', views.house_page, name='single_product'),
    path('products/offers/<str:group>/<str:filterby>/<str:filter>/', views.offers, name='offers_list'),
    path('dashboard/', views.Dashboard.as_view(), name='dashboard'),
    path('homes/review/<str:unique_home_hash>/', views.AuditHomeAdmin.as_view(), name='review_home'),
    path('homes/review/user/<str:unique_home_hash>', views.AuditHomeUser.as_view(), name='review_home_user'),
    path('homes/<str:status>/', views.AdminHomeList.as_view(), name='review_list'),
    path('homes/<str:action>/<str:unique_home_hash>', views.takeActionOnHome, name='take_action_on_home'),
    path('homes/', views.UserHomeList.as_view(), name='user_homes_list'),
    path('homes/confirm/on-site/<str:home_unique_hash>/', views.UserConfirmHomeOnSite.as_view(), name='confirm_home_on_site'),
    path('homes/confirm/on-sale/<str:home_unique_hash>/', views.ConfirmHomeOnSale.as_view(), name='confirm_home_on_sale'),
]
