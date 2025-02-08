from django.shortcuts import render
from authlib.integrations.django_client import OAuth
from django.shortcuts import redirect
from django.contrib.auth import login as auth_login
from django.contrib.auth import get_user_model
from django.views import View
from django.http import JsonResponse
from django.conf import settings
from django.urls import reverse


# Create your views here.

User = get_user_model()
# Initialize OAuth client
oauth = OAuth()

# Set up Google OAuth client
google = oauth.register(
    'google',
    client_id=settings.AUTH0_CLIENT_ID,
    client_secret=settings.AUTH0_CLIENT_SECRET,
    authorize_url=f'https://{settings.AUTH0_DOMAIN}/authorize',
    access_token_url=f'https://{settings.AUTH0_DOMAIN}/oauth/token',
    api_base_url=f'https://{settings.AUTH0_DOMAIN}/userinfo',
    client_kwargs={
        'scope': 'openid profile email',
    },
)

class GoogleLoginView(View):
    """
    This view handles the login process for users via Google Sign-In.
    It redirects users to Okta/Auth0's authorization endpoint.
    """
    def get(self, request, *args, **kwargs):
        """
        Redirect the user to Google login for authentication.
        """
        # Construct the redirect URL for Google login
        redirect_uri = request.build_absolute_uri(reverse('google_callback'))
        return google.authorize_redirect(request, redirect_uri)


class GoogleCallbackView(View):
    """
    This view handles the callback from Google Sign-In via Okta/Auth0.
    It fetches the user's information and registers/logs them in.
    """
    def get(self, request, *args, **kwargs):
        token = google.authorize_access_token(request)
        user_info = google.parse_id_token(token)

        user_email = user_info.get('email')
        user_first_name = user_info.get('given_name')
        user_last_name = user_info.get('family_name')

        # Use email as the unique identifier instead of username
        user, created = User.objects.get_or_create(
            email=user_email,
            defaults={'username': user_email, 'first_name': user_first_name, 'last_name': user_last_name}
        )

        auth_login(request, user)
        return redirect('/dashboard/')  # Change this to your actual dashboard URL


