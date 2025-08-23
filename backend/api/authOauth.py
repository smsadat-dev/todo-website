import os, requests
import json

from django.http import JsonResponse
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import RefreshToken

User = get_user_model()

GOOGLE_CLIENT_ID = os.getenv("GOOGLE_KEY")
GOOGLE_CLIENT_SECRET = os.getenv("GOOGLE_SECRET")
GOOGLE_REDIRECT_URI = os.getenv("GOOGLE_REDIRECT_URI")  # frontend URL that receives token


def googleLogin(request):
    """
    Return URL for frontend to redirect user to Google's OAuth consent screen
    """

    oauth_url = (
        f"https://accounts.google.com/o/oauth2/v2/auth"
        f"?response_type=code"
        f"&client_id={GOOGLE_CLIENT_ID}"
        f"&redirect_uri={GOOGLE_REDIRECT_URI}"
        f"&scope=openid email profile"
    )
    return JsonResponse({'auth_url': oauth_url})



def googleCallback(request):
    
    body = json.loads(request.body)
    code = body.get("code")
    if not code:
        return JsonResponse({'status':'error','message':'Missing code'}, status=400)

    # Exchange code for tokens
    token_res = requests.post(
        "https://oauth2.googleapis.com/token",
        data={
            "code": code,
            "client_id": GOOGLE_CLIENT_ID,
            "client_secret": GOOGLE_CLIENT_SECRET,
            "redirect_uri": GOOGLE_REDIRECT_URI,
            "grant_type": "authorization_code",
        }
    ).json()

    access_token = token_res.get("access_token")
    if not access_token:
        return JsonResponse({'status':'error','message':'Failed to get token'}, status=400)

    # Get user info
    userinfo = requests.get(
        "https://www.googleapis.com/oauth2/v3/userinfo",
        headers={"Authorization": f"Bearer {access_token}"}
    ).json()

    email = userinfo.get("email")
    username = email.split("@")[0]

    user, _ = User.objects.get_or_create(email=email, defaults={'username': username})
    refresh = RefreshToken.for_user(user)

    return JsonResponse({
        "status": "success",
        "access": str(refresh.access_token),
        "refresh": str(refresh),
        "username": user.username
    })
