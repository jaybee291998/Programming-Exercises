from .models import Lesson
from datetime import datetime, timedelta
import pytz

from rest_framework import status
from rest_framework.response import Response 
from rest_framework.decorators import api_view

# for json response
from django.http import JsonResponse
import json

from .serializers import DeadlineSerializer


# a function that get all the lessons that will have a deadline
# witihin a given time range
@api_view(['GET', 'POST'])
def get_lesson(request):
	if request.method == 'POST':
		deadline_serializer = DeadlineSerializer(data=request.data)
		if deadline_serializer.is_valid():
			start_date = deadline_serializer.validated_data.get('start_date')
			end_date = deadline_serializer.validated_data.get('end_date')
			print(start_date)
			print(end_date)

			lessons = Lesson.objects.filter(deadline__range=[start_date, end_date])

			# loop through all the lessons that has a deadline in between the time range
			for lesson in lessons:
				# loop through all the student work of the lesson to check wether a student submitted there work before the dealine
				for student_work in lesson.studentwork.all():
					# if the student hasnt turned in there work yet mark them as late
					if not student_work.turned_in:
						student_work.late = True 
						student_work.save()


			data = []
			for lesson in lessons:
				data.append({
					'title':lesson.title,
					'deadline':lesson.deadline
					})

			return JsonResponse(list(data), safe=False)