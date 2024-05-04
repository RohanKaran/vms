import json

from django.urls import reverse
from django.utils import timezone
from rest_framework import status
from rest_framework.test import APITestCase

from api.purchase_orders.models import PurchaseOrder
from api.vendors.models import Vendor


class PurchaseOrderTestCase(APITestCase):
    def setUp(self):
        self.vendor = Vendor.objects.create(
            name="Test Vendor",
            contact_details="info@testvendor.com",
            address="400 Vendor St, Vendor City, VC 10000",
            vendor_code="VEND004",
        )
        self.purchase_order = PurchaseOrder.objects.create(
            po_number="PO123456",
            vendor=self.vendor,
            order_date="2022-01-01T00:00:00Z",
            expected_delivery_date="2022-01-10T00:00:00Z",
            delivery_date=None,
            items=json.dumps({"item1": "10", "item2": "20"}),
            quantity=30,
            status="pending",
        )

    def test_create_purchase_order(self):
        """
        Ensure we can create a new purchase order.
        """
        url = reverse("purchaseorder-list")
        data = {
            "po_number": "PO123457",
            "vendor": self.vendor.id,
            "order_date": "2022-01-02T00:00:00Z",
            "expected_delivery_date": "2022-01-11T00:00:00Z",
            "items": json.dumps({"item3": "15", "item4": "25"}),
            "quantity": 40,
            "status": "ordered",
        }
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(PurchaseOrder.objects.count(), 2)

    def test_retrieve_purchase_order(self):
        """
        Ensure we can retrieve a purchase order's details.
        """
        url = reverse("purchaseorder-detail", args=[self.purchase_order.id])
        response = self.client.get(url, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["po_number"], "PO123456")

    def test_update_purchase_order(self):
        """
        Ensure we can update an existing purchase order using PATCH for partial updates.
        """
        url = reverse("purchaseorder-detail", args=[self.purchase_order.id])
        updated_data = {"status": "completed", "delivery_date": "2022-01-09T00:00:00Z"}
        response = self.client.patch(url, updated_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        updated_po = PurchaseOrder.objects.get(id=self.purchase_order.id)
        self.assertEqual(updated_po.status, "completed")
        self.assertEqual(
            updated_po.delivery_date.strftime("%Y-%m-%dT%H:%M:%SZ"),
            "2022-01-09T00:00:00Z",
        )

    def test_list_purchase_orders(self):
        """
        Ensure we can list all purchase orders and filter by vendor.
        """
        url = reverse("purchaseorder-list")
        response = self.client.get(url, {"vendor": self.vendor.id}, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)  # Assuming only one PO for this vendor

    def test_delete_purchase_order(self):
        """
        Ensure we can delete a purchase order.
        """
        url = reverse("purchaseorder-detail", args=[self.purchase_order.id])
        response = self.client.delete(url, format="json")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(PurchaseOrder.objects.count(), 0)

    def test_acknowledge_purchase_order(self):
        self.purchase_order.issue_date = timezone.now() - timezone.timedelta(hours=1)
        self.purchase_order.save()

        url = reverse('acknowledge_purchase_order', args=[self.purchase_order.id])
        response = self.client.post(url, format='json')

        self.purchase_order.refresh_from_db()
        acknowledgment_time = self.purchase_order.acknowledgment_date.timestamp()
        current_time = timezone.now().timestamp()
        self.assertTrue(abs(acknowledgment_time - current_time) < 10)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.vendor.refresh_from_db()
        self.assertTrue(self.vendor.average_response_time > 0)
