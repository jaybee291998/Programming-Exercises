import os

from celery import Celery

# set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'lms.settings')

app = Celery('lms')

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object('django.conf:settings', namespace='CELERY')

app.conf.beat_schedule = {
	'check-lesson-deadline':{
		'task':'lms.task.check_deadline',
		'schedule':600,
		'args':(15,)
	},
	'send-advance-email-notif':{
		'task':'lms.task.send_one_day_advance_deadline_notif',
		'schedule':3600,
		'args':(70,)
	}
}

# Load task modules from all registered Django app configs.
app.autodiscover_tasks()


@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')
