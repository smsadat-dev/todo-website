import json

from django.http import JsonResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.utils.timezone import localtime
from django.views.decorators.csrf import csrf_exempt

from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.token_blacklist.models import BlacklistedToken, OutstandingToken

from .models import TaskModel

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


    if request.method == "OPTIONS":
        # Preflight request for CORS
        response = JsonResponse({"status": "ok"})
        response["Access-Control-Allow-Origin"] = "*"
        response["Access-Control-Allow-Methods"] = "POST, GET, DELETE, OPTIONS"
        response["Access-Control-Allow-Headers"] = "Authorization, Content-Type"
        return response


    jwt_auth = JWTAuthentication()
    auth_result = jwt_auth.authenticate(request)

    if auth_result is None:
        return JsonResponse({'status': 'error', 'message': 'Invalid or missing token'}, status=401)

    user, validate_token = auth_result

    # show all the tasks to do of requested user in a list

    if request.method == 'GET':
        tasks = TaskModel.objects.filter(user=user).values('id', 'title', 'description', 'creationTime', 'completed')
        return JsonResponse({
            'status': 'success',
            'tasks': list(tasks),
        }, safe=False)        

    elif request.method == 'POST':
        body = json.loads(request.body)
        taskTitle = body.get('tasksTitle')
        taskDesc = body.get('tasksDescrp')
        
        task = TaskModel(
            user = user,
            title = taskTitle,
            description = taskDesc
        )
        task.save()
        task_id = getattr(task, 'id', getattr(task, 'pk', None))

        return JsonResponse({
            'status': 'success',
            'message': 'Task created successfully',
            'task': {
                'taskID': task_id,
                'taskTitle': taskTitle,
                'taskDesc': taskDesc,
                'creationTime': localtime(task.creationTime).strftime('%Y-%m-%d %H:%M:%S'),
                'isDone': task.completed,
            }
        })
    
    elif request.method == 'DELETE':
        
        try: 
            data = json.loads(request.body)
            task_id = data.get('task_id')
            if not task_id:
                return JsonResponse({'status': 'error', 'message': 'task_id missing'}, status=400)
 
        except (json.JSONDecodeError, AttributeError):
            return JsonResponse({'status': 'error', 'message': 'Invalid request'}, status=400)

        # delete only if task belongs to requested user
        try:
            task = TaskModel.objects.filter(user=user, id=task_id)
            task.delete()
            return JsonResponse({'status': 'success', 'message': 'Task deleted'})
        
        except TaskModel.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Task not found'}, status=404)

    else:
        return JsonResponse({'status': 'error', 'message': 'Invalid request method'})
    
    

# Google Oauth
def google_callback(request):
    user = request.user
    refresh = RefreshToken.for_user(user)

    return JsonResponse({
        'status': 'success',
        'access': str(refresh.access_token),
        'refresh': str(refresh),
        'username': user.username,
    })