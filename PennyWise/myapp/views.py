from django.shortcuts import render
from authlib.integrations.django_client import OAuth
from django.shortcuts import redirect
from django.contrib.auth import login as auth_login
from django.contrib.auth import get_user_model
from django.views import View
from django.http import JsonResponse
from django.conf import settings
from django.urls import reverse
from urllib.parse import quote_plus, urlencode
import json
import os
import base64
import hashlib

# Create your views here.

User = get_user_model()
# Initialize OAuth client
oauth = OAuth()

# Set up Google OAuth client
oauth.register(
    "auth0",
    client_id=settings.AUTH0_CLIENT_ID,
    client_secret=settings.AUTH0_CLIENT_SECRET,
    client_kwargs={
        "scope": "openid profile email",
    },
    server_metadata_url=f"https://{settings.AUTH0_DOMAIN}/.well-known/openid-configuration",
)


class LoginView(View):
    """
    This view handles the login process for users via Google Sign-In.
    It redirects users to Okta/Auth0's authorization endpoint.
    """
    def get(self, request, *args, **kwargs):
        """
        Redirect the user to Google login for authentication.
        """
        # Generate a nonce (random string) and store it in the session
        nonce = base64.urlsafe_b64encode(os.urandom(32)).decode('utf-8')
        request.session['nonce'] = nonce

        # Construct the redirect URL for Auth0 login
        return oauth.auth0.authorize_redirect(
            request,
            request.build_absolute_uri(reverse("callback")),
            nonce=nonce  # Include the nonce here
        
    )


class CallbackView(View):
    """
    This view handles the callback from Google Sign-In via Okta/Auth0.
    It fetches the user's information and registers/logs them in.
    """
    def get(self, request, *args, **kwargs):
        token = oauth.auth0.authorize_access_token(request)
        request.session["user"] = token

        # Retrieve the nonce from the session
        nonce = request.session.get('nonce')

        # # Parse the ID token and pass the nonce for verification
        user_info = oauth.auth0.parse_id_token(token, nonce=nonce)

        # Extract user data
        user_email = user_info.get('email')
        user_first_name = user_info.get('given_name')
        user_last_name = user_info.get('family_name')

        # Check if user exists in the database
        user, created = User.objects.get_or_create(
            username=user_email,
            defaults={
                'first_name': user_first_name,
                'last_name': user_last_name,
                'email': user_email,
            }
        )

        # Log the user in
        auth_login(request, user)

        # Redirect to the index or dashboard page
        return redirect(request.build_absolute_uri(reverse("index")))


class LogoutView(View):
    """
    This view handles logging out the user by clearing the session and redirecting
    to Auth0's logout endpoint.
    """
    def get(self, request, *args, **kwargs):
        request.session.clear()
        return redirect(
            f"https://{settings.AUTH0_DOMAIN}/v2/logout?"
            + urlencode(
                {
                    "returnTo": request.build_absolute_uri(reverse("index")),
                    "client_id": settings.AUTH0_CLIENT_ID,
                },
                quote_via=quote_plus,
            ),
        )


class IndexView(View):
    """
    This view renders the home page and displays the user's session data if logged in.
    """
    def get(self, request, *args, **kwargs):
        return render(
            request,
            "index.html",
            context={
                "session": request.session.get("user"),
                "pretty": json.dumps(request.session.get("user"), indent=4),
            },
        )