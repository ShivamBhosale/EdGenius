from .models import NewUser, Courses
from django.contrib.auth.forms import UserCreationForm
from django import forms


class SignUpForm(UserCreationForm):
    class Meta:
        model = NewUser
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2', 'user_type')


class CoursesForm(forms.ModelForm):
    class Meta:
        model = Courses
        fields = ['course_name', 'description', 'course_image', 'course_tag', 'instructor',
                  'course_video', 'course_files']
