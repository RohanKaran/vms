from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import VendorViewSet, VendorPerformanceView

router = DefaultRouter()
router.register(r"", VendorViewSet)

urlpatterns = [
    path("", include(router.urls)),
    path(
        "<int:vendor_id>/performance/",
        VendorPerformanceView.as_view(),
        name="vendor-performance",
    ),
]
