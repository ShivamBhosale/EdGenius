from datetime import date

from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views import View
from django.contrib.auth.forms import UserCreationForm
from django.views.generic.edit import CreateView

from EdGeniusApp.decorators import redirect_if_logged_in
from EdGeniusApp.mixins import RedirectIfLoggedInMixin
from django.shortcuts import render
from django.contrib.auth.views import LoginView, LogoutView, PasswordResetView
from django.urls import reverse_lazy, reverse
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect,get_object_or_404
from .forms import SignUpForm,CoursesForm
from .models import NewUser, Student, CourseEnrolled, Attendance, Grades, Courses
from django.core.exceptions import ValidationError
import razorpay
from EdGenius import settings
from django.contrib.auth.models import User, Group




class LoginInterfaceView(RedirectIfLoggedInMixin, LoginView):
    template_name = 'EdGeniusApp/login.html'

    def form_valid(self, form):
        # Call the parent class's form_valid method to perform the default login action
        response = super().form_valid(form)

        # Now, you can set the session data
        self.request.session['username'] = self.request.user.username
        self.request.session['first_name'] = self.request.user.first_name
        self.request.session['email'] = self.request.user.email
        # You can store any other user-specific data you need in the session.

        return response
    def get_success_url(self):
        success_url = super().get_success_url()

        # Get the user_type of the logged-in user from the database
        try:
            user_type = NewUser.objects.get(username=self.request.user.username).user_type
        except NewUser.DoesNotExist:
            user_type = None

        if user_type == "Student":
            membership = Student.objects.get(email=self.request.user.email).membership
            if membership == "Gold" or membership == "Silver" or membership == "Bronze":
                return '/shomepage/'
            else:
                return '/membership_options/'

        elif user_type == "Instructor":
            return '/ihomepage/'
        else:
            raise ValidationError('You are not a registered Student or Instructor')

class StudentHomeView(LoginRequiredMixin, TemplateView):
    template_name = 'EdGeniusApp/student_homepage.html'

    def get(self, request, *args, **kwargs):
        # Get the stored username from the session
        username = request.session.get('username', None)
        first_name = request.session.get('first_name', None)

        # Do something with the username and age
        context = {'username': username, 'first_name': first_name}
        return render(request, self.template_name, context)


class InstructorHomeView(LoginRequiredMixin, TemplateView):
    template_name = 'EdGeniusApp/instructor_homepage.html'


class LogoutInterfaceView(LoginRequiredMixin, LogoutView):
    template_name = 'EdGeniusApp/logout.html'


class AuthorizedView(LoginRequiredMixin, TemplateView):
    template_name = 'EdGeniusApp/authorized.html'
    login_url = '/EdGeniusApp/login.html'


@redirect_if_logged_in
def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.refresh_from_db()
            # load the profile instance created by the signal
            user.save()
            raw_password = form.cleaned_data.get('password1')
            user_type = form.cleaned_data.get('user_type')

            # login user after signing up
            user = authenticate(username=user.username, password=raw_password)
            login(request, user)

            if user_type == "Student":
            # redirect user to student home page
                return redirect('EdGeniusApp:student_home')
            else:
                return redirect('EdGeniusApp:instructor_home')
    else:
        form = SignUpForm()
    return render(request, 'EdGeniusApp/signup.html', {'form': form})


class PasswordResetInterfaceView(PasswordResetView):
    template_name = 'EdGeniusApp/password_reset_form.html'
    email_template_name = 'EdGeniusApp/password_reset_email.html'
    success_url = reverse_lazy("EdGeniusApp:password_reset_done")


@login_required
def membership_options(request):
    total_amount = 0
    if request.method == 'POST':
        selected_membership = request.POST.get('selected_membership')
        if selected_membership == 'Gold':
            total_amount = 80
        elif selected_membership == 'Silver':
            total_amount = 50
        elif selected_membership == 'Bronze':
            total_amount = 30
        client = razorpay.Client(auth=(settings.KEY_ID,settings.KEY_SECRET))
        payment = client.order.create({'amount': total_amount, 'currency':'CAD', 'payment_capture':1})
        context = {'membership': selected_membership, 'payment':payment}
        print("Payment:",payment )
    return render(request, 'EdGeniusApp/membership_options.html')


@login_required
def handle_payment_success(request):
    if request.method == 'POST':
        username = Student.objects.get(user__username=request.user.username)
        response = request.POST# Assuming you are receiving the Razorpay response here
        membership_type = request.POST.get('membership_type')  # Retrieve the membership type from the payment form
        username.membership_type = membership_type
        username.save(update_fields=['membership_type'])

        return JsonResponse({'message': 'Payment successful!'})
    return JsonResponse({'message': 'Invalid request.'}, status=400)


@login_required
def student_attendance(request, course_name):

    student_list = Student.objects.filter(courseenrolled__course__course_name=course_name)

    if request.method == 'POST':
        student_instance = Student.objects.filter(user__username=request.session.get('username',None)).first()
        course_instance = Courses.objects.filter(course_name=course_name).values('id').first()
        course_id = course_instance['id']
        username = student_instance
        attendance = request.POST.get('attendance')

        up_attend = Attendance(
            student=username,
            course_id=course_id,
            attendance=attendance,
            date=date.today()
        )
        up_attend.save()
        return render(request,'EdGeniusApp/attendance.html', {'student_list': student_list, 'course_name': course_name})
    return render(request, 'EdGeniusApp/attendance.html', {'student_list': student_list, 'course_name': course_name})

@login_required
def my_courses(request):
    return render(request, 'EdGeniusApp/my_courses.html')

@login_required
def update_attendance(request,course_name):
    student_list = Student.objects.filter(courseenrolled__course__course_name=course_name)

    if request.method == 'POST':
        student_instance = Student.objects.filter(user__username=request.session.get('username', None)).first()
        course_instance = Courses.objects.filter(course_name=course_name).values('id').first()
        course_id = course_instance['id']
        username = student_instance
        attendance = request.POST.get('attendance')

        up_attend = Attendance(
            student=username,
            course_id=course_id,
            attendance=attendance,
            date=date.today()
        )
        up_attend.save()
        return render(request, f'EdGenius/attendance.html/{course_name}')

    #print('not going')
    return render(request, f'EdGeniusApp/attendance.html/{course_name}', {'student_list': student_list})


# fetching attendance for course wise
@login_required
def fetch_attendance(request, course_name):
    student_list = Student.objects.filter(courseenrolled__course__course_name=course_name)
    return render(request,'EdGeniusApp/fetch_attendance.html', {'student_list': student_list,'course_name': course_name})


# fetching attendance for individual student
@login_required
def fetch_attendance_student(request, course_name):
    student_email = request.GET.get('select-student-name-dropdown', False)
    # print(student_email)
    if student_email:
            individual_student = Attendance.objects.filter(course__course_name=course_name).filter(student__email=student_email)
            # course_id = individual_student[0].course
            student_list = Student.objects.filter(attendance__course__course_name=course_name)
            return render(request, 'EdGeniusApp/fetch_attendance.html', {'individual_student': individual_student, 'course_name':course_name,
                                                                  'student_list': student_list, 'student_email': student_email})

    return render(request, 'EdGeniusApp/fetch_attendance.html')

#This will update grades for student
@login_required
def grade_page(request, course_name):
    student_list = Student.objects.filter(courseenrolled__course__course_name=course_name)

    if request.method == 'POST':
        student_instance = Student.objects.filter(firstname=request.POST.get('fname')).first()
        course_instance = Courses.objects.filter(course_name=course_name).values('id').first()
        course_id = course_instance['id']
        username = student_instance
        grade_item = request.POST.get('gradeitem')
        grades = request.POST.get('grades')
        feedback = request.POST.get('feedback')

        # print(f'firstname: {firstname} type:{type(firstname)}')
        # print(f'laststname: {lastname} type:{type(lastname)}')
        # print(f'email: {email} type:{type(email)}')
        # print(f'course: {course} ')
        # print(f'gradeItem: {gradeItem} ')
        # print(f'grades: {grades} ')
        # print(f'feedback: {feedback} ')

        update_grade = Grades(
            student=username,
            course_id=course_id,
            gradeItem=grade_item,
            grade=grades,
            feedback=feedback,
        )
        update_grade.save()
        return render(request, 'EdGeniusApp/grades_provider.html', {'student_list': student_list,'course': course_name})

    return render(request,'EdGeniusApp/grades_provider.html',{'student_list': student_list, 'course': course_name})

class CheckStudentGrades(LoginRequiredMixin, View):
    def get(self, request, course_name):
        student_list = Student.objects.filter(courseenrolled__course__course_name=course_name)

        if request.method == 'GET':
            student_name = 'blank'
            student_email = request.GET.get('select-student-grades-dropdown')
            print(student_email)
            individual_student_grades = Grades.objects.filter(course__course_name=course_name).filter(student__email=student_email)
            if individual_student_grades:
                student_name = individual_student_grades[0].student.firstname + ' '+individual_student_grades[0].student.lastname
            return render(request, 'EdGeniusApp/check_student_grades.html',
                          {'student_list': student_list, 'course_name': course_name,
                           'individual_student_grades': individual_student_grades, 'student_name': student_name })

        return render(request,'EdGeniusApp/check_student_grades.html',{'student_list': student_list,'course_name': course_name})




# def checkStudentGrade(request,course_name):
#     student_list = Grades.objects.filter(course=course_name)
#     if student_list:
#         return render(request, 'myapp1/check_student_grades.html',
#                   {'student_list': student_list, 'course_name': course_name})
#
#     return render(request, 'myapp1/check_student_grades.html')

class ViewMyGrades(LoginRequiredMixin, View):
    def get(self, request, course_name):
        student_username = request.session.get('username', None)  # change this according to the current user
        student_name = request.session.get('firstname', None)  # change this according to the current user
        grades = Grades.objects.filter(course__course_name=course_name).filter(student__user__username=student_username)
        if grades:
            return render(request,'EdGeniusApp/view_my_grades.html',{'grades': grades,'course_name': course_name, 'student_name': student_name})
        return render(request, 'EdGeniusApp/view_my_grades.html',{'course_name': course_name})


class ViewMyAttendance(LoginRequiredMixin, View):
    def get(self,request,course_name):
        student_username = request.session.get('username', None) # change this according to teh current user
        student_name = request.session.get('firstname', None) # change this according to teh current user
        attendance = Attendance.objects.filter(course__course_name=course_name).filter(student__user__username=student_username)
        if attendance:
            return render(request,'EdGeniusApp/view_my_attendance.html',{'attendance': attendance,'course_name': course_name,'student_name': student_name})
        return render(request, 'EdGeniusApp/view_my_attendance.html',{'course_name': course_name})
    


# Shivam_view

class Index(TemplateView):
    template_name = 'EdGeniusApp/index.html'

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
    