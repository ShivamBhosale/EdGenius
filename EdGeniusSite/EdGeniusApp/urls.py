from django.urls import path, reverse_lazy
from django.contrib.auth import views as auth_views
from . import views
from django.conf import settings
from django.conf.urls.static import static
app_name = 'EdGeniusApp'

urlpatterns = [
    path('',views.Index.as_view(), name='index'),
    path('homepage/', views.StudentHomeView.as_view(), name='student_home'),
    #path('ihomepage/', views.InstructorHomeView.as_view(), name='instructor_home'),
    path('login/', views.LoginInterfaceView.as_view(), name='login'),
    path('logout/', views.LogoutInterfaceView.as_view(), name='logout'),
    path('authorized/', views.AuthorizedView.as_view(), name='authorized'),
    path('signup/', views.SignUpView.as_view(), name='signup'),
    path('password_reset/', views.PasswordResetInterfaceView.as_view(), name='password_reset'),
    path('password_reset_done/', auth_views.PasswordResetDoneView.as_view(template_name ='EdGeniusApp/password_reset_done.html'),
         name='password_reset_done'),
    path('password_reset_confirm/<uidb64>/<token>', auth_views.PasswordResetConfirmView.as_view(template_name ='EdGeniusApp/password_reset_confirm.html', success_url = reverse_lazy("EdGeniusApp:password_reset_complete")),
         name='password_reset_confirm'),
    path('password_reset_complete/', auth_views.PasswordResetCompleteView.as_view(template_name ='EdGeniusApp/password_reset_complete.html'), name='password_reset_complete'),
    path('instructor_homepage/', views.InstructorHomepageView.as_view(), name='instructor_homepage'),
    path('student_homepage/', views.StudentHomepageView.as_view(), name='student_homepage'),
    path('add/', views.add_course, name='add_course'),
    path('<slug:course_slug>/', views.CourseDetailView.as_view(), name='course_detail'),
    
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)