from django.urls import path, include

from . import views

app_name = 'api'

urlpatterns = [
    path('login/', views.usrLogin),
    path('registration/', views.userRegistration),
    path('logout/', views.userLogout),
    path('tasks/', views.processTasks),
    path('auth/', include('allauth.urls')), # for Oauth
]