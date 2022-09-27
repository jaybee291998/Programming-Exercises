from django.urls import path, include
from .views import login_view, register_view, edit_profile_view, verification_view, logout_view, login_api_view
from rest_framework.authtoken.views import obtain_auth_token
from . import views

from django.contrib.auth import views as auth_views
urlpatterns = [
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('register/', register_view, name='register'),
    path('edit-profile/', edit_profile_view, name='edit_profile'),
    path('verification/<uidb64>/<token>/', verification_view, name='verification'),
    path('login-api/', login_api_view, name='login_api'),
    path('resend-verification-link/', views.resend_verification_link, name='resend-verification-link'),

    # for token
    path('api-token-auth/', obtain_auth_token, name='api_token_auth'),

    
	# password reset paths
    path('password-reset/', auth_views.PasswordResetView.as_view(template_name='accounts/password_reset.html'), name="password_reset"),
    path('password-reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='accounts/password_reset_done.html'), name="password_reset_done"),
    path('password-reset-confirm/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='accounts/password_reset_confirm.html'), name="password_reset_confirm"),
    path('password-reset-complete/', auth_views.PasswordResetCompleteView.as_view(template_name='accounts/password_reset_complete.html'), name="password_reset_complete")
]