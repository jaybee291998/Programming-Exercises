from django.urls import path, include
from .views import createclass_view, myclasses_view, specificclass_view, invite_student_view, accept_invite_view, grade_sheet_view, student_search_view
from . import views
from .api import get_search_result
from . import api
urlpatterns = [
    path('create-class/', createclass_view, name='create-class'),
    path('myclasses/', myclasses_view, name='myclasses_view'),
    path('specific-class/<class_id>/', specificclass_view, name='specific-class'),
    path('specific-class/<class_id>/stream/', views.specificclass_stream_view, name='specific-class-stream'),
    path('specific-class/<class_id>/classwork/', views.specificclass_classwork_view, name='specific-class-classwork'),
    path('specific-class/<class_id>/people/', views.specificclass_people_view, name='specific-class-people'),
    path('specific-class/<class_id>/grade/', views.specificclass_grade_view, name='specific-class-grade'),
    path('delete-class/<class_id>/', views.delete_class_view, name='delete-class'),
    path('invite-student/<class_id>/', invite_student_view, name='invite-student'),
    path('accept-invite/<class_id>/<class_token>/<student_id>/', accept_invite_view, name='accept-invite'),
    path('grade-sheet/<class_id>', grade_sheet_view, name='grade_sheet'),
    path('student-search/', student_search_view, name='student-search'),
    path('join-class/<class_id>/<class_token>/', views.join_class_view, name='join-class'),
    path('accept-student/<class_id>/<class_token>/<student_id>/', views.accept_student_view, name='accept-student'),
    path('get-search-result/', get_search_result, name='get-search-result'),
    path('get-grades/<class_id>/', api.get_grades, name='get-grades'),
    path('unenroll-student/<class_id>/<student_id>/', views.unenroll_student_view, name='unenroll-student'),
    path('change-banner/<class_id>/', views.change_class_banner_view, name='change-banner')
]