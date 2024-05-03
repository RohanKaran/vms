from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import PurchaseOrderViewSet

router = DefaultRouter()
router.register(r"", PurchaseOrderViewSet)

urlpatterns = [
    path("", include(router.urls)),
]
