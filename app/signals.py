from django.contrib.auth.signals import user_logged_in
from django.dispatch import receiver
from .models import UserProfile  # Import the UserProfile model

@receiver(user_logged_in)
def on_user_logged_in(sender, request, user, **kwargs):
    session_key = request.session.session_key
    user_profile, created = UserProfile.objects.get_or_create(user=user)
    user_profile.session_key = session_key
    user_profile.save()