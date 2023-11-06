from django.utils import timezone
from django.contrib.sessions.models import Session


class SessionTimeoutMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.user.is_authenticated:
            # Update the session expiry time on each request
            session_key = request.session.session_key
            if session_key:
                session = Session.objects.filter(session_key=session_key).first()
                if session:
                    session_expiry = timezone.now() + timezone.timedelta(seconds=request.session.get_expiry_age())
                    session.expire_date = session_expiry
                    session.save()

        response = self.get_response(request)
        return response