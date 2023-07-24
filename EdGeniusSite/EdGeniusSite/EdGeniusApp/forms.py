from .models import NewUser,Courses,CourseFile
from django.contrib.auth.forms import UserCreationForm
from django import forms


class SignUpForm(UserCreationForm):
    class Meta:
        model = NewUser
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2', 'user_type')


class CoursesForm(forms.ModelForm):
    
    class Meta:
        model = Courses
        fields = ['CourseName','courseID', 'description', 'course_image', 'course_tag', 'instructorName', 'course_video','course_files']
        