from django.shortcuts import redirect

from EdGeniusApp.models import NewUser


def redirect_if_logged_in(view_func):
    def _wrapped_view(request, *args, **kwargs):
        if request.user.is_authenticated:
            user_type = NewUser.objects.get(username=request.user.username).user_type
            if user_type == "Student":
                # redirect user to student home page
                return redirect('EdGeniusApp:student_home')
            else:
                return redirect('EdGeniusApp:instructor_home')
        return view_func(request, *args, **kwargs)

    return _wrapped_view