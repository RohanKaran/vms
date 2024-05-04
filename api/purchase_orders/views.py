from django.utils import timezone
from rest_framework import status, viewsets
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import PurchaseOrder
from .serializers import PurchaseOrderSerializer


class PurchaseOrderViewSet(viewsets.ModelViewSet):
    queryset = PurchaseOrder.objects.all()
    serializer_class = PurchaseOrderSerializer


class AcknowledgePurchaseOrderAPIView(APIView):
    def post(self, request, po_id):
        try:
            purchase_order = PurchaseOrder.objects.get(pk=po_id)
        except PurchaseOrder.DoesNotExist:
            return Response(
                {"error": "Purchase Order not found"}, status=status.HTTP_404_NOT_FOUND
            )

        purchase_order.acknowledgment_date = timezone.now()
        purchase_order.save()

        self.update_response_time(purchase_order.vendor)

        return Response(
            {"message": "Purchase Order acknowledged successfully"},
            status=status.HTTP_200_OK,
        )

    def update_response_time(self, vendor):
        pos = PurchaseOrder.objects.filter(
            vendor=vendor, acknowledgment_date__isnull=False
        )
        response_times = [po.acknowledgment_date - po.issue_date for po in pos]
        if response_times:
            total_seconds = sum([rt.total_seconds() for rt in response_times])
            average_response_time = total_seconds / len(response_times)
        else:
            average_response_time = 0

        vendor.average_response_time = average_response_time
        vendor.save()
