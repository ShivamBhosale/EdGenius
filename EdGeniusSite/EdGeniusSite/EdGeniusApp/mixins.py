from django.shortcuts import redirect
from django.urls import reverse

from EdGeniusApp.models import NewUser


class RedirectIfLoggedInMixin:
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            try:
                user_type = NewUser.objects.get(username=request.user.username).user_type
                if user_type == "Student":
                    # redirect user to student home page
                    return redirect('EdGeniusApp:student_home')
                else:
                    return redirect('EdGeniusApp:instructor_home')
            except:
                raise ValueError("User Type doesn't exist")

        return super().dispatch(request, *args, **kwargs)