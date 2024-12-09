from django.utils import timezone

from huey import crontab
from huey.contrib import djhuey as huey

from .models import ProductOrder
from utils.telegram import report_to_admin


@huey.db_periodic_task(crontab(hour="10", minute="16"), retries=2, retry_delay=10)
def delete_orders_with_no_customers():
    qs = ProductOrder.objects.filter(
        created_on__lt=timezone.now() - timezone.timedelta(days=1),
        customer=None,
    )
    report_to_admin(f"✅ Deleted {qs.count()} Product orders with no customers")
    qs.delete()
