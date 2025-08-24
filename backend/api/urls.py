from django.urls import path, include

from . import views
from .authOauth import googleLogin, googleCallback

app_name = 'api'

urlpatterns = [
    path('login/', views.usrLogin, name='login'),
    path('registration/', views.userRegistration, name='registration'),
    path('logout/', views.userLogout, name='logout'),
    path('tasks/', views.processTasks, name='tasks'),

    path('api/auth/google/', include('allauth.socialaccount.providers.google.urls')),

    path('auth/google/login/', googleLogin, name="google_login"),
    path('auth/google/callback/', googleCallback, name="google_callback"),
]