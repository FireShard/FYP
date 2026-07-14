from django.urls import path, include
from . import views
from rest_framework import routers

router = routers.DefaultRouter()
router.register(r'UserLaptop', views.UserLaptopViewSet)
router.register(r'LaptopDetails', views.LaptopDetailsViewSet)


urlpatterns = [
    path('', include(router.urls)),
]
