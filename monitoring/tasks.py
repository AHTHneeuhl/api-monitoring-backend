import time
import requests

from celery import shared_task
from django.utils import timezone

from .models import MonitoredAPI
from .models import APILog


@shared_task
def monitor_apis():
    """
    Celery background task that checks all registered APIs.

    Steps:
    1. Fetch active APIs
    2. Send HTTP request
    3. Measure response time
    4. Save APILog
    """

    apis = MonitoredAPI.objects.filter(is_active=True)

    logs = []

    for api in apis:

        start_time = time.time()

        try:
            response = requests.get(api.url, timeout=10)

            response_time = int((time.time() - start_time) * 1000)

            log = APILog(
                monitored_api=api,
                status_code=response.status_code,
                response_time_ms=response_time,
                is_success=response.status_code < 500,
                checked_at=timezone.now(),
            )

        except Exception as error:

            response_time = int((time.time() - start_time) * 1000)

            log = APILog(
                monitored_api=api,
                status_code=0,
                response_time_ms=response_time,
                is_success=False,
                error_message=str(error),
                checked_at=timezone.now(),
            )

        logs.append(log)

    # Bulk insert for performance
    APILog.objects.bulk_create(logs)