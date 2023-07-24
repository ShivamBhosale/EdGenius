from django.contrib import admin
from .models import NewUser, Student, Instructor, Courses, CourseEnrolled, Attendance, Grades, CourseFile

admin.site.register(NewUser)
admin.site.register(Student)
admin.site.register(Instructor)
admin.site.register(Courses)
admin.site.register(CourseEnrolled)
admin.site.register(Attendance)
admin.site.register(Grades)
admin.site.register(CourseFile)
#admin.site.register(Membership)