#!/bin/bash
# Deletes customers who haven't ordered in a year and logs the cleanup.

set -e
cd "$(dirname "$0")/../.."

python3 manage.py shell <<EOF
from django.utils import timezone
from datetime import timedelta
from crm.models import Customer

one_year_ago = timezone.now() - timedelta(days=365)

# Find customers who have NO orders in the last year
inactive_customers = Customer.objects.exclude(
    id__in=Customer.objects.filter(
        orders__created_at__gte=one_year_ago
    ).values_list('id', flat=True)
)

count = inactive_customers.count()
inactive_customers.delete()

print(f"{count} inactive customers deleted on {timezone.now()}.")
EOF

echo "\$(date '+%Y-%m-%d %H:%M:%S') - Cleanup completed" >> /tmp/customer_cleanup_log.txt
chmod +x crm/cron_jobs/clean_inactive_customers.sh
