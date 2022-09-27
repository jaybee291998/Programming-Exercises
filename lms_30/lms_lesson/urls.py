from django.urls import path, include
from .views import add_new_lesson_view, add_lesson_file_view, specific_lesson_view
from . import views
from .api import get_lesson

urlpatterns = [
    path('add-new-lesson/<class_id>/', add_new_lesson_view, name='add-new-lesson'),
    path('add-lecture/<class_id>/<type_of_lecture>', views.add_lecture_view, name='add-lecture'),
    path('add-lesson-file/<lesson_id>', add_lesson_file_view, name='add-lesson-file'),
    path('add-lecture-file/<lecture_id>/', views.add_lecture_file_view, name='add-lecture-file'),
    path('edit-lesson/<lesson_id>/', views.edit_lesson_view, name='edit-lesson'),
    path('edit-lecture/<lecture_id>/', views.edit_lecture_view, name='edit-lecture'),
    path('delete-lesson/<lesson_id>/', views.delete_lesson, name='delete-lesson'),
    path('delete-lecture/<lecture_id>/', views.delete_lecture, name='delete-lecture'),
    path('delete-lecture-file/<lecture_file_id>/<lecture_id>/', views.delete_lecture_file_view, name='delete-lecture-file'),
    path('specific-lesson/<lesson_id>', specific_lesson_view, name='specific-lesson'),
    path('specific-lecture/<lecture_id>', views.specific_lecture_view, name='specific-lecture'),
    path('delete-lesson-file/<lesson_file_id>/<lesson_id>/', views.delete_lesson_file_view, name='delete-lesson-file'),
    path('get-lesson/', get_lesson, name='get-lesson'),
    path('get-lesson-view/', views.get_lesson_view, name='get-lesson-view')
]