#!/bin/bash
#from datetime import date
cd "$(dirname "$0")/../.."

TIMESTAMP=$(date "+%Y-%m-%d %H:%M:%S")

DELETED_COUNT=$(python manage.py shell <<'EOF'
from datetime import timedelta, date
from django.utils import timezone
from crm.models import Customer, Order

one_year_ago=timezone.now() - timedelta(days=365)
inactive_customers=Customer.objects.exclude(
id__in=Order.objects.filter(order_date__gte=one_year_ago).values_list('customer_id', flat=True)
)
count, _ = inactive_customers.delete()
print(count if count else 0)
EOF
)
LOG_FILE="./tmp/customer_cleanup_log.txt"
echo "[$TIMESTAMP] Deleted $DELETED_COUNT inactive customers"
echo "[$TIMESTAMP] Deleted $DELETED_COUNT inactive customers" >>"$LOG_FILE"