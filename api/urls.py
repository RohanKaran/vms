from django.urls import include, path

urlpatterns = [
    path("vendors/", include("api.vendors.urls")),
    path("purchase_orders/", include("api.purchase_orders.urls")),
]
