# forms.py
from django import forms
from .models import Courses,CourseFile

class CoursesForm(forms.ModelForm):
    
    class Meta:
        model = Courses
        fields = ['CourseName','courseID', 'description', 'course_image', 'course_tag', 'instructorName', 'course_video','course_files']
        


