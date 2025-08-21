from django.urls import path

from . import views

app_name = 'api'

urlpatterns = [
    path('login/', views.usrLogin),
    path('registration/', views.userRegistration),
    path('logout/', views.userLogout),
    path('tasks/', views.processTasks),
]