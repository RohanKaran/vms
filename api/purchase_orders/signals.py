from django.db.models import F
from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver

from .models import PurchaseOrder


@receiver(post_save, sender=PurchaseOrder)
@receiver(post_delete, sender=PurchaseOrder)
def update_vendor_performance(sender, instance, **kwargs):
    if instance.vendor:
        vendor = instance.vendor
        update_performance_metrics(vendor)


def update_performance_metrics(vendor):
    pos = PurchaseOrder.objects.filter(vendor=vendor)
    completed_pos = pos.filter(status="completed")

    on_time_deliveries = completed_pos.filter(
        delivery_date__lte=F("order_date")
    ).count()
    if completed_pos.count() > 0:
        vendor.on_time_delivery_rate = on_time_deliveries / completed_pos.count()
    else:
        vendor.on_time_delivery_rate = 0

    quality_ratings = [
        po.quality_rating for po in completed_pos if po.quality_rating is not None
    ]
    if quality_ratings:
        vendor.quality_rating_avg = sum(quality_ratings) / len(quality_ratings)
    else:
        vendor.quality_rating_avg = 0

    response_times = [
        po.acknowledgment_date - po.issue_date
        for po in pos
        if po.acknowledgment_date is not None
    ]
    if response_times:
        total_seconds = sum([rt.total_seconds() for rt in response_times])
        vendor.average_response_time = total_seconds / len(response_times)
    else:
        vendor.average_response_time = 0

    successful_fulfillments = pos.filter(status="completed").count()
    if pos.count() > 0:
        vendor.fulfillment_rate = successful_fulfillments / pos.count()
    else:
        vendor.fulfillment_rate = 0

    vendor.save()
