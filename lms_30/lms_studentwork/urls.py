from django.urls import path, include
# from .views import student_work_view
from . import views
urlpatterns = [
	# path('student-work/<student_work_id>/', student_work_view, name='student_work'),
	path('delete-student-file/<student_file_id>/<student_work_id>/', views.delete_student_file_view, name='delete-student-file'),
	path('student-work-mark/<student_work_id>/', views.student_work_mark_view, name='student-work-mark'),
	path('student-work-file/<student_work_id>/', views.student_work_file_view, name='student-work-file'),
	path('student-work-comment/<student_work_id>/', views.student_work_comment_view, name='student-work-comment')
]