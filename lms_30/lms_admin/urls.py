from django.urls import path, include
from . import views
	

urlpatterns = [
    path('add-new-announcement', views.add_new_announcement_view, name='add-new-announcement'),
    path('add-announcement-image/<announcement_id>/', views.add_announcement_image_view, name='add-announcement-image'),
    path('specific-announcement/<announcement_id>/', views.specific_announcement_view, name='specific-announcement'),
    path('my-announcements/', views.my_announcements_view, name='my-announcements'),
    path('announcement-showcase/', views.announcement_showcase_view, name='announcement-showcase'),
    path('edit-annoucement/<announcement_id>/', views.edit_announcement_view, name='edit-announcement'),
    path('delete-announcement/<announcement_id>/', views.delete_announcement_view, name='delete-announcement'),
    path('delete-announcement-image/<announcement_image_id>/<announcement_id>/', views.delete_announcement_image_view, name='delete-announcement-image'),
    path('request-instructorship/', views.request_instructorship_view, name='request-instructorship'),
    path('instructors/', views.instructors_view, name='instructors'),
    path('pending-instructors/', views.pending_instructors_view, name='pending-instructors'),
    path('accept-instructor/<instructor_id>/', views.accept_instructor_view, name='accept-instructor'),
    path('revoke-instructorship/<instructor_id>/', views.revoke_instructorship_view, name='revoke-instructorship'),
    path('deny-instructor/<instructor_id>/', views.deny_instructor_view, name='deny-instructor')
]

