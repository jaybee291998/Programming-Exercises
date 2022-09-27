from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings
from time import sleep

from lms_lesson.models import Lesson
from datetime import datetime, timedelta

import pytz

SINGAPORE_TZ = pytz.timezone('Asia/Singapore')

@shared_task
def sleepy(duration):
	sleep(duration)
	return None

@shared_task
def send_email_task(subject, body, receivers):
	send_mail(
		subject,
		body,
		settings.EMAIL_HOST_USER,
		receivers
	)
	return None

@shared_task
def periodic_message(message):
	print(f'This should appear every 15 seconds: {message}')

@shared_task
def check_deadline(minutes): 
	end_date = SINGAPORE_TZ.localize(datetime.now())
	start_date = end_date-timedelta(minutes=minutes)

	# get all the lessons that haved reached there deadline from 15 minutes ago until now
	lessons_deadlined = Lesson.objects.filter(deadline__range=[start_date, end_date])
	# loop through all the lessons that has a deadline in between the time range
	for lesson in lessons_deadlined:
		# loop through all the student work of the lesson to check wether a student submitted there work before the dealine
		for student_work in lesson.studentwork.all():
			# if the student hasnt turned in there work yet mark them as late
			if not student_work.turned_in:
				student_work.late = True 
				student_work.save()
	print(minutes)
	return f'from {start_date} to {end_date} with {len(lessons_deadlined)} updated lessons'

# send an advance email notification to all the students that have an approaching deadline within a day
@shared_task
def send_one_day_advance_deadline_notif(offset_minutes):
	start_date = SINGAPORE_TZ.localize(datetime.now() + timedelta(days=1))
	end_date = start_date + timedelta(minutes=offset_minutes)
	# get all the lessons that have a deadline within the range of 1 day from now to 1 day and n=hours hour from now
	lessons_with_deadline_within_range = Lesson.objects.filter(deadline__range=[start_date, end_date])

 	# loop trhiugh all the lessons that have a deadline within the range
	for lesson in lessons_with_deadline_within_range:
 		email_subject = 'Deadline Reminder'
 		body = f"Your '{lesson.type_of_lesson}:{lesson.title}' in class '{lesson.lesson_class}' has a deadline within 24 hours,\n If you haven't submitted your work yet please submit within 24 hours, if you have please disregard this message"
 		receiver_emails = [user.email for user in lesson.lesson_class.students.all()]
 		send_email_task(email_subject, body, receiver_emails)
	return f'from {start_date} to {end_date} with {len(lessons_with_deadline_within_range)} lessons'