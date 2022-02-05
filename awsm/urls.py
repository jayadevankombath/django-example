from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('coupons/', include('coupons.urls'), name='coupons'),
    path('adminawsm/', include('adminawsm.urls'), name="awsm_admin"),
    path('admin/', admin.site.urls),
]
