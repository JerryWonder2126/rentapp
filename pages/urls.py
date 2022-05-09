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
    path('homes/review/<str:unique_id>', views.reviewHomeStaff, name='review_home'),
    path('homes/review/user/<str:unique_id>', views.reviewHomeUser, name='review_home_user'),
    path('homes/review/<str:status>/', views.AdminHomeList.as_view(), name='review_list'),
    # path('homes/review/started/', views.listHomesForReview, {'group': 'started'}, name='started_review_list'),
    # path('homes/review/updated/', views.listHomesForReview, {'group': 'updated'}, name='updated_review_list'),
    # path('homes/review/onsite/', views.listHomesForReview, {'group': 'on_site'}, name='onsite_review_list'),
    # path('homes/review/passed/', views.listHomesPassedReview, name='passed_review_list'),
    # path('homes/sale/fresh/', views.listHomesOnSale, name='on_sale_list'),
    # path('homes/sale/ongoing/', views.listHomesTransactionOngoing, name='transaction_ongoing_list'),
    # path('homes/sale/completed/', views.listHomesSold, name='sold_list'),
    path('homes/', views.UserHomeList.as_view(), name='user_homes_list'),
    path('homes/confirm/on-site/', views.userConfirmHome, {'confirm_type': 'on_site'}, name='confirm_home_on_site'),
    path('homes/confirm/on-sale/', views.userConfirmHome, {'confirm_type': 'on_sale'}, name='confirm_home_on_sale'),
]
