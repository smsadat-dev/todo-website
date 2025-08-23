from django.urls import path, include

from . import views
from .authOauth import googleLogin, googleCallback

app_name = 'api'

urlpatterns = [
    path('login/', views.usrLogin),
    path('registration/', views.userRegistration),
    path('logout/', views.userLogout),
    path('tasks/', views.processTasks),

    path('api/auth/google/', include('allauth.socialaccount.providers.google.urls')),

    path('auth/google/login/', googleLogin, name="google_login"),
    path('auth/google/callback/', googleCallback, name="google_callback"),
]