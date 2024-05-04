from django.db.models import F
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver

from .models import PurchaseOrder


@receiver(pre_save, sender=PurchaseOrder)
def pre_save_purchase_order(sender, instance, **kwargs):
    if instance.pk:
        old_po = PurchaseOrder.objects.get(pk=instance.pk)
        instance._old_status = old_po.status
    else:
        instance._old_status = None


@receiver(post_save, sender=PurchaseOrder)
def update_vendor_performance(sender, instance, created, **kwargs):
    old_status = getattr(instance, "_old_status", None)
    new_status = instance.status
    if old_status != new_status and (
        new_status == "completed" or old_status == "completed"
    ):
        if instance.vendor:
            update_performance_metrics(instance.vendor)


def update_performance_metrics(vendor):
    pos = PurchaseOrder.objects.filter(vendor=vendor)
    completed_pos = pos.filter(status="completed")

    on_time_deliveries = completed_pos.filter(
        delivery_date__lte=F("expected_delivery_date")
    ).count()
    if completed_pos.count() > 0:
        vendor.on_time_delivery_rate = on_time_deliveries / completed_pos.count() * 100
    else:
        vendor.on_time_delivery_rate = 0

    quality_ratings = [
        po.quality_rating for po in completed_pos if po.quality_rating is not None
    ]
    if quality_ratings:
        vendor.quality_rating_avg = sum(quality_ratings) / len(quality_ratings)
    else:
        vendor.quality_rating_avg = 0

    successful_fulfillments = pos.filter(status="completed").count()
    if pos.count() > 0:
        vendor.fulfillment_rate = successful_fulfillments / pos.count() * 100
    else:
        vendor.fulfillment_rate = 0

    vendor.save()
