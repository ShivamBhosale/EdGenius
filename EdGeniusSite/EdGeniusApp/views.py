from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render
from django.contrib.auth.views import LoginView, LogoutView, PasswordResetView
from django.urls import reverse_lazy
from django.views.generic import TemplateView
from django.views.generic.edit import CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from .models import Courses
from .forms import CoursesForm
from django.shortcuts import render, redirect, get_object_or_404

class Index(TemplateView):
    template_name = 'EdGeniusApp/index.html'

    
class LoginInterfaceView(LoginView):
    template_name = 'EdGeniusApp/login.html'


class StudentHomeView(TemplateView, LoginRequiredMixin):
    template_name = 'EdGeniusApp/student_homepage.html'
#
# class InstructorHomeView(TemplateView, LoginRequiredMixin):
#     template_name = 'EdGeniusApp/instructor_homepage.html'

class LogoutInterfaceView(LogoutView, LoginRequiredMixin):
    template_name = 'EdGeniusApp/logout.html'


class AuthorizedView(TemplateView, LoginRequiredMixin):
    template_name = 'EdGeniusApp/authorized.html'
    login_url = '/EdGeniusApp/login.html'


class SignUpView(CreateView):
    form_class = UserCreationForm
    template_name = 'EdGeniusApp/signup.html'
    success_url = 'EdGeniusApp/login'

    def get(self, request, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect('EdGeniusApp:student_home')
        return super().get(request, *args, **kwargs)


class PasswordResetInterfaceView(PasswordResetView):
    template_name = 'EdGeniusApp/password_reset_form.html'
    email_template_name = 'EdGeniusApp/password_reset_email.html'
    success_url = reverse_lazy("EdGeniusApp:password_reset_done")

class InstructorHomepageView(TemplateView, LoginRequiredMixin):
    
    def get(self, request):
        course_list = Courses.objects.all().order_by()
        return render(request,'EdGeniusApp/instructor_homepage.html',{'course_list': course_list})
# class CreateCourseView(TemplateView, LoginRequiredMixin):
#     def get(self, request):
#         course_list = Courses.objects.all().order_by()
#         return render(request,'EdGeniusApp/create_course.html',{'course_list': course_list})

    
class StudentHomepageView(TemplateView, LoginRequiredMixin):
    def get(self, request):
        course_list = Courses.objects.all().order_by()
        return render(request,'EdGeniusApp/student_homepage.html',{'course_list': course_list})
    

# views.py


def add_course(request):
    if request.method == 'POST':
        form = CoursesForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('../instructor_homepage/')  # Replace 'course_list' with the URL name of the page listing all courses
    else:
        form = CoursesForm()

    return render(request, 'EdGeniusApp/add_course.html', {'form': form})


class MembershipView(TemplateView):
    def get(self, request):
        return render(request,'EdGeniusApp/membership_login.html')
    
class AddCourseFiles(TemplateView):
     def get(self, request, course_slug):
        course = get_object_or_404(Courses, slug=course_slug)
        return render(request,'EdGeniusApp/add_courseFiles.html', {'course':course})


class CourseDetailView(TemplateView):
    def get(self, request, course_slug):
        # course = Courses.objects.get(slug=course_slug)
        # # course_list = get_object_or_404(Courses, slug=course_slug)
        # return render(request, 'EdGeniusApp/course_detail.html', {'course': course})
        course = get_object_or_404(Courses, slug=course_slug)
        
        return render(request, 'EdGeniusApp/course_detail.html', {'course': course})
class CourseDetailViewStudent(TemplateView):
    def get(self, request, course_slug):
        # course = Courses.objects.get(slug=course_slug)
        # # course_list = get_object_or_404(Courses, slug=course_slug)
        # return render(request, 'EdGeniusApp/course_detail.html', {'course': course})
        course = get_object_or_404(Courses, slug=course_slug)
        return render(request, 'EdGeniusApp/course_detailStudent.html', {'course': course})
    


