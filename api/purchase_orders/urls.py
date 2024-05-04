from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import AcknowledgePurchaseOrderAPIView, PurchaseOrderViewSet

router = DefaultRouter()
router.register(r"", PurchaseOrderViewSet)

urlpatterns = [
    path("", include(router.urls)),
    path(
        "<int:po_id>/acknowledge/",
        AcknowledgePurchaseOrderAPIView.as_view(),
        name="acknowledge_purchase_order",
    ),
]
