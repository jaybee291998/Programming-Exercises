from rest_framework import status
from rest_framework.response import Response 
from rest_framework.decorators import api_view

# for json response
from django.http import JsonResponse
import json

from django.contrib.auth import get_user_model
# the user model
User = get_user_model()

from .serializers import SearchResultSerializer, SearchInputSerializer


from django.contrib.auth.decorators import login_required
#models
from .models import LMSClass
from lms_studentwork.models import StudentWork
# libraries needed to encode and decode id's
from django.utils.encoding import force_bytes, force_text, DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse


@api_view(['POST', 'GET'])
def get_search_result(request):
	if request.method == 'POST':
		search_input_serializer = SearchInputSerializer(data=request.data)
		if search_input_serializer.is_valid():
			# print(search_input_serializer.validated_data.get('search_input'))
			term = search_input_serializer.validated_data.get('search_input')
			qs = User.objects.filter(profile__first_name__istartswith=term) | User.objects.filter(profile__last_name__istartswith=term) | User.objects.filter(email__istartswith=term) | User.objects.filter(profile__course__icontains=term) | User.objects.filter(profile__year__icontains=term)
			# result_serializer = SearchResultSerializer()
			search_results = []
			for user in qs:
				search_results.append({
					'email':user.email,
					'first_name':user.profile.first_name,
					'last_name':user.profile.last_name,
					'course':user.profile.course,
					'year':user.profile.year
					})
			return JsonResponse(list(search_results), safe=False)


@api_view(['GET'])
def get_grades(request, class_id):
	try:
		decoded_class_id = force_bytes(urlsafe_base64_decode(class_id))
		specific_class = LMSClass.objects.get(pk=decoded_class_id)
	except(LMSClass.DoesNotExist):
		specific_class = None

	if specific_class is not None:
		if request.user == specific_class.instructor:
			# get all the lessons of the class
			lessons = specific_class.lesson.all()
			students = specific_class.students.all()
			data = extract_grades(specific_class.lesson.filter(type_of_lesson='QZ'), students)
			# all the lesson types
			lesson_types = ['QZ', 'AS', 'AC', 'EX']
			# the terms
			terms = ['PRE', 'MID', 'SEM', 'FIN']

			class_grades = {}
			for term in terms:
				term_grades = {}
				for lesson_type in lesson_types:
					lesson_type_grades = extract_grades(specific_class.lesson.filter(type_of_lesson=lesson_type, term=term), students)
					term_grades[lesson_type] = lesson_type_grades
				class_grades[term] = term_grades

			class_grades['class_details'] = {
				'name':specific_class.name
			}


			return JsonResponse(list([class_grades]), safe=False)
		else:
			return JsonResponse(list([{'message':'You are not the instructo of this class'}]), safe=False)

# hepler functions

# extract grades from each lesson for every student
def extract_grades(lessons, students):
	data = {}
	for student in students:
		grades = {}
		for lesson in lessons:
			grades[lesson.type_of_lesson+'#'+' '+str(lesson.num)] = StudentWork.objects.get(lesson=lesson, student=student).mark
		data[student.profile.first_name] = grades

	return data
