from django.contrib import admin
from .models import Admin, Announcement, AnnouncementImage
# Register your models here.

admin.site.register(Admin)
admin.site.register(Announcement)
admin.site.register(AnnouncementImage)
