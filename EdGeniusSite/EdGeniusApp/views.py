from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render
from django.contrib.auth.views import LoginView, LogoutView, PasswordResetView
from django.urls import reverse_lazy
from django.views.generic import TemplateView
from django.views.generic.edit import CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect

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

