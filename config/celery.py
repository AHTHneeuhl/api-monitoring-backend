# config/celery.py

import os
from celery import Celery

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings.local")

app = Celery("api_monitoring")

app.config_from_object("django.conf:settings", namespace="CELERY")

app.autodiscover_tasks()


# Celery Beat Schedule
app.conf.beat_schedule = {
    "monitor-apis-every-60-seconds": {
        "task": "monitoring.tasks.dispatch_monitoring_tasks",
        "schedule": 60.0,  # every 60 seconds
    },
}


@app.task(bind=True)
def debug_task(self):
    print(f"Request: {self.request!r}")