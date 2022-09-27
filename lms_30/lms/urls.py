"""lms URL Configurationa

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include

from django.conf import settings
from django.conf.urls.static import static

from .views import home_view

from django.views.generic import TemplateView

from lms_admin.views import announcement_showcase_view as showcase

	

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('accounts.urls')),
    path('lmsclass/', include('lms_class.urls')),
    path('lmslesson/', include('lms_lesson.urls')),
    path('lmsstudentwork/', include('lms_studentwork.urls')),
    path('lmsadmin/', include('lms_admin.urls')),
    path('home/', showcase, name='home'),
    path('', showcase, name='announcement-showcase'),
    path('', TemplateView.as_view(template_name='index.html'))
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
