from django.contrib import admin
from .models import NewUser, Student, Instructor, Membership, CourseFile, Courses, CourseEnrolled, Attendance, Grades

admin.site.register(NewUser)
admin.site.register(Student)
admin.site.register(Instructor)
admin.site.register(Membership)
admin.site.register(Courses)
admin.site.register(CourseEnrolled)
admin.site.register(Attendance)
admin.site.register(Grades)
admin.site.register(CourseFile)