# monitoring/tasks.py

import time
import requests

from celery import shared_task
from django.utils import timezone

from apis.models import MonitoredAPI
from monitoring.models import APILog


@shared_task
def dispatch_monitoring_tasks():
    """
    Scheduler task.

    This task finds all active APIs and
    dispatches monitoring jobs to Celery workers.
    """

    apis = MonitoredAPI.objects.filter(is_active=True).values_list("id", flat=True)

    for api_id in apis:
        check_api_health.delay(api_id)


@shared_task
def check_api_health(api_id: int):
    """
    Checks a single API endpoint.

    Steps:
    1. Fetch API
    2. Send HTTP request
    3. Measure response time
    4. Store APILog
    """

    try:
        api = MonitoredAPI.objects.get(id=api_id, is_active=True)
    except MonitoredAPI.DoesNotExist:
        return

    start_time = time.time()

    try:
        response = requests.get(api.url, timeout=10)

        response_time = int((time.time() - start_time) * 1000)

        APILog.objects.create(
            monitored_api=api,
            status_code=response.status_code,
            response_time_ms=response_time,
            is_success=response.status_code < 500,
            checked_at=timezone.now(),
        )

    except Exception as error:

        response_time = int((time.time() - start_time) * 1000)

        APILog.objects.create(
            monitored_api=api,
            status_code=0,
            response_time_ms=response_time,
            is_success=False,
            error_message=str(error),
            checked_at=timezone.now(),
        )