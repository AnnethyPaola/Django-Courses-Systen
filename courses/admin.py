from xml.dom import ValidationErr
from django.contrib import admin
from .models import Courses, GroupClass, Students,Teacher
# Register your models here.
admin.site.register(Courses)
admin.site.register(Teacher)
admin.site.register(Students)
admin.site.register(GroupClass)
class StudentsAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name')

