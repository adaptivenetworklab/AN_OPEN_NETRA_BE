from django.contrib.auth import logout
from django.contrib.sessions.models import Session
from .models import UserProfile

class OneSessionPerUserMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.user.is_authenticated:
            try:
                user_profile = UserProfile.objects.get(user=request.user)
                if user_profile.session_key and user_profile.session_key != request.session.session_key:
                    Session.objects.filter(session_key=user_profile.session_key).delete()
                    logout(request)
            except UserProfile.DoesNotExist:
                pass
        response = self.get_response(request)
        return response