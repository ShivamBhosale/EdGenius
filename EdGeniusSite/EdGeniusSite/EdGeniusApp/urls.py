from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, reverse_lazy
from django.contrib.auth import views as auth_views
from . import views

app_name = 'EdGeniusApp'

urlpatterns = [
    path('',views.Index.as_view(), name='index'),
    path('payment/', views.PaymentGateway.as_view(), name='payment'),
    path('charge/<int:amount>',views.charge, name='charge'),
    path('shomepage/', views.StudentHomeView.as_view(), name='student_home'),
    path('ihomepage/', views.InstructorHomeView.as_view(), name='instructor_home'),
    path('login/', views.LoginInterfaceView.as_view(), name='login'),
    path('logout/', views.LogoutInterfaceView.as_view(), name='logout'),
    path('authorized/', views.AuthorizedView.as_view(), name='authorized'),
    path('signup/', views.signup, name='signup'),
    path('password_reset/', views.PasswordResetInterfaceView.as_view(), name='password_reset'),
    path('password_reset_done/', auth_views.PasswordResetDoneView.as_view(template_name ='EdGeniusApp/password_reset_done.html'),
         name='password_reset_done'),
    path('password_reset_confirm/<uidb64>/<token>', auth_views.PasswordResetConfirmView.as_view(template_name ='EdGeniusApp/password_reset_confirm.html', success_url = reverse_lazy("EdGeniusApp:password_reset_complete")),
         name='password_reset_confirm'),
    path('password_reset_complete/', auth_views.PasswordResetCompleteView.as_view(template_name ='EdGeniusApp/password_reset_complete.html'), name='password_reset_complete'),
    path('handle_payment_success/', views.handle_payment_success, name='payment_success'),
    path('attendance/<str:course_name>', views.student_attendance, name='student_attendance'),
    path('update_attendance/<str:course_name>', views.update_attendance, name='update_attendance'),
    path('my_courses/', views.my_courses, name='my_courses'),
    path('fetch_attendance/<str:course_name>', views.fetch_attendance, name='fetch_attendance'),
    path('fetchstudent/<str:course_name>', views.fetch_attendance_student, name='fetchstudent'),
    path('grades_provider/<str:course_name>', views.grade_page, name='grades_provider'),
    path('check_student_grades/<str:course_name>', views.CheckStudentGrades.as_view(), name='check_student_grades'),
#    path('check_student_grades/<str:course_name>', views.CheckStudentGrades.as_view(), name='check_grades'),
    path('view_my_grades/<str:course_name>', views.ViewMyGrades.as_view(), name='my_grades'),
    path('view_my_attendance/<str:course_name>', views.ViewMyAttendance.as_view(), name='my_attendance'),
    path('add_course/', views.add_course, name='add_course'),
    path('<slug:course_slug>/add_courseFiles', views.AddCourseFiles.as_view(), name='add_courseFiles'),
    path('<slug:course_slug>/', views.CourseDetailView.as_view(), name='course_detail'),
    path('<slug:course_slug>/student', views.CourseDetailViewStudent.as_view(),
                       name='course_detailStudent'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)