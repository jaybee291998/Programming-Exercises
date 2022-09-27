from django.contrib import admin
from .models import StudentWork, StudentWorkFile, StudentWorkComment
# Register your models here.

admin.site.register(StudentWork)
admin.site.register(StudentWorkFile)
admin.site.register(StudentWorkComment)
