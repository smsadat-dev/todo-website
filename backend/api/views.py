import json

from django.http import JsonResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt

from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.token_blacklist.models import BlacklistedToken, OutstandingToken


@csrf_exempt  # used JWT instead
def usrLogin(request):

    if request.method != 'POST':
        return JsonResponse({'status': 'error', 'message': 'Invalid request method'})

    username = request.POST.get('username')
    password = request.POST.get('password')

    user = authenticate(username=username, password=password)

    if user is None:
        return JsonResponse({'status': 'error', 'message': 'Invalid credentials'})

    # create JWT token

    refresh = RefreshToken.for_user(user)
    login(request, user)
    return JsonResponse({
        'status': 'success',
        'access': str(refresh.access_token),
        'refresh': str(refresh),
        'username': user.username,
    })

@csrf_exempt # used JWT instead
def userRegistration(request):

    if request.method != 'POST':
        return JsonResponse({'status': 'error', 'message': 'Invalid request method'})

    username = request.POST.get('username')
    password1 = request.POST.get('password1')
    password2 = request.POST.get('password2')
    email = request.POST.get('email')

    if not username or not password1 or not password2 or not email:
        return JsonResponse({'status': 'error', 'message': 'All fields are required'})
    
    if password1 != password2:
        return JsonResponse({'status': 'error', 'message': 'Passwords don\'t match'})
    
    if User.objects.filter(username=username):
        return JsonResponse({'status': 'error', 'message': 'Username taken'})
    
    user = User.objects.create_user(username=username, password=password1, email=email)

    return JsonResponse({'status': 'success', 'message': 'Congratulations! You are registered'})


@csrf_exempt # used JWT instead
def userLogout(request):
    if request.method != 'POST':
        return JsonResponse({'status': 'error', 'message': 'Invalid request method'})
    
    try:
        body = json.loads(request.body)
        refreshToken = body.get('refresh')

        if not refreshToken:
            return JsonResponse({'status': 'error', 'message': 'Refresh token required'})

        token = RefreshToken(refreshToken)
        token.blacklist()

        return JsonResponse({'status': 'success', 'message': 'You are logged out'})

    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)})
    

@csrf_exempt # used JWT instead
def processTasks(request):

    # show all the tasks to do of requested user in a list
    if request.method == 'GET':


    elif request.method == 'POST':

    elif request.method == 'PUT':

    elif request.method == 'PATCH':

    elif request.method == 'DELETE':
    
    else:
        return JsonResponse({'status': 'error', 'message': 'Invalid request method'})
    
    