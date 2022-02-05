from django.urls import path
from .import views

urlpatterns = [
    path('',views.coupons_list, name="coupons"),
    path('add/', views.coupons_add, name="coupons_add"),
    path('edit/<int:id>/', views.coupon_edit, name="coupon_edit"),
    path('update/<int:id>/', views.update_coupon, name="update_coupon"),
    path('approve/<int:id>/', views.coupon_approve, name="coupon_edit"),
    path('delete/<int:id>/', views.coupon_delete, name="coupon_delete"),
]