from django.contrib import admin
from lms_lesson.models import Lesson, LessonFile, Lecture, LectureFile, LectureComment
# Register your models here.

admin.site.register(Lesson)
admin.site.register(LessonFile)
admin.site.register(Lecture)
admin.site.register(LectureFile)
admin.site.register(LectureComment)
