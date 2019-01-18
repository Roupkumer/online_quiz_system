from django.contrib import admin
from .models import Teacher, Student, Course,Notice
# Register your models here.

admin.site.register(Student)
admin.site.register(Teacher)
admin.site.register(Course)
admin.site.register(Notice)
