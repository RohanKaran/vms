import json
from datetime import UTC, datetime, timedelta

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from api.purchase_orders.models import PurchaseOrder
from api.vendors.models import Vendor


class VendorTestCase(APITestCase):
    def setUp(self):
        self.vendor1 = Vendor.objects.create(
            name="Vendor One",
            contact_details="contact@vendorone.com",
            address="100 One St, Town, TX 70001",
            vendor_code="VEND001",
        )
        self.vendor2 = Vendor.objects.create(
            name="Vendor Two",
            contact_details="info@vendortwo.com",
            address="200 Two St, City, CY 80002",
            vendor_code="VEND002",
        )

    def test_create_vendor(self):
        """
        Ensure we can create a new vendor.
        """
        url = reverse("vendor-list")
        data = {
            "name": "New Vendor",
            "contact_details": "new@vendor.com",
            "address": "300 New St, Village, VG 90003",
            "vendor_code": "VEND003",
        }
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Vendor.objects.count(), 3)
        self.assertEqual(Vendor.objects.get(id=3).name, "New Vendor")

    def test_retrieve_vendor(self):
        """
        Ensure we can retrieve a vendor's details.
        """
        url = reverse("vendor-detail", args=[self.vendor1.id])
        response = self.client.get(url, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["name"], "Vendor One")

    def test_update_vendor(self):
        """
        Ensure we can update an existing vendor.
        """
        url = reverse("vendor-detail", args=[self.vendor1.id])
        updated_data = {
            "name": "Vendor One Updated",
            "contact_details": "updated@vendorone.com",
            "address": "100 One St, Town, TX 70001",
            "vendor_code": "VEND001",
        }
        response = self.client.put(url, updated_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            Vendor.objects.get(id=self.vendor1.id).name, "Vendor One Updated"
        )

    def test_list_vendors(self):
        """
        Ensure we can list all vendors.
        """
        url = reverse("vendor-list")
        response = self.client.get(url, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)  # Assuming we have 2 vendors

    def test_delete_vendor(self):
        """
        Ensure we can delete a vendor.
        """
        url = reverse("vendor-detail", args=[self.vendor2.id])
        response = self.client.delete(url, format="json")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Vendor.objects.count(), 1)


class VendorPerformanceTestCase(APITestCase):
    def setUp(self):
        # Create a vendor
        self.vendor = Vendor.objects.create(
            name="Performance Vendor",
            contact_details="contact@performancevendor.com",
            address="500 Performance St, Metric City, MC 20000",
            vendor_code="PERF001",
        )
        order_date = datetime.now(UTC) - timedelta(days=10)
        delivery_date = order_date + timedelta(days=5)
        self.po1 = PurchaseOrder.objects.create(
            po_number="PO10001",
            vendor=self.vendor,
            order_date=order_date,
            expected_delivery_date=delivery_date,
            delivery_date=delivery_date - timedelta(days=1),  # Delivered 1 day early
            items=json.dumps({"item1": "5", "item2": "15"}),
            quantity=20,
            status="completed",
            quality_rating=4.5,
        )
        self.po2 = PurchaseOrder.objects.create(
            po_number="PO10002",
            vendor=self.vendor,
            order_date=order_date,
            expected_delivery_date=delivery_date,
            delivery_date=delivery_date + timedelta(days=2),  # Delivered 2 days late
            items=json.dumps({"item3": "10", "item4": "20"}),
            quantity=30,
            status="completed",
            quality_rating=4.0,
        )

    def test_retrieve_vendor_performance_metrics(self):
        """
        Ensure we can retrieve the performance metrics for a specific vendor.
        """
        url = reverse("vendor-performance", args=[self.vendor.id])
        response = self.client.get(url, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("on_time_delivery_rate", response.data)
        self.assertIn("quality_rating_avg", response.data)
        self.assertIn("average_response_time", response.data)
        self.assertIn("fulfillment_rate", response.data)

        expected_on_time_delivery_rate = 50
        expected_quality_rating_avg = (4.5 + 4.0) / 2
        self.assertEqual(
            response.data["on_time_delivery_rate"], expected_on_time_delivery_rate
        )
        self.assertEqual(
            response.data["quality_rating_avg"], expected_quality_rating_avg
        )
