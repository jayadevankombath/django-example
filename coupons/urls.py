from django.urls import path
from .import views

urlpatterns = [
    path('', views.approved_coupons, name="my_view"),
    path('scrap/', views.scrap_coupons, name="coupon_scraping"),

]