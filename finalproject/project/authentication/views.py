
import json
from django.http import HttpResponse, JsonResponse
from django.shortcuts import redirect, render
from django.contrib.auth.models import User
from django.urls import reverse
from django.views.decorators.http import require_POST
from validate_email_address import validate_email
from django.contrib import messages
from django.db.models import Q
from django.contrib.auth import authenticate ,login ,logout

# Create your views here.
def Login(request):
    page = 'login'
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request,'Username not found')
        
        user = authenticate(username=username,password=password)
        if user is not None:
            login(request,user)
            return redirect('index')
        else:
            messages.error(request,"Invalid Credentials")
        
    context ={'page':page}
    return render(request,'authentication/login_register.html',context)


@require_POST
def login_api(request):
    data = json.loads(request.body)
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return JsonResponse({'error': 'Username and password are required'}, status=400)

    user = authenticate(username=username, password=password)
    if user is not None:
        login(request, user)
        return JsonResponse({'message': 'Login successfull'}, status=200)
    else:
        return JsonResponse({'error': 'Invalid credentials'}, status=401)



def Logout(request):
    logout(request)
    messages.info(request,"Logout Sucessfull")
    return redirect('login')
    

def Registration(request):
    if request.method == "POST":

        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']

        if not User.objects.filter(username=username).exists():
            if not User.objects.filter(email=email).exists():
                if len(password) < 6:
                    context={'fieldValues':request.POST}
                    messages.error(request,'Password is short')
                    return render(request,'authentication/login_register.html',context)
            
            user = User.objects.create_user(username=username,email=email)

            user.set_password(password)
            user.save()
            return redirect('login')
        
    return render(request,'authentication/login_register.html')

@require_POST
def registration_api(request):
    data = json.loads(request.body)
    username = data['username']
    email = data['email']
    password = data['password']

    if User.objects.filter(username=username).exists():
        return JsonResponse({'error': 'Username is already taken'}, status=400)

    if User.objects.filter(email=email).exists():
        return JsonResponse({'error': 'Email is already registered'}, status=400)

    if len(password) < 6:
        return JsonResponse({'error': 'Password is too short'}, status=400)

    user = User.objects.create_user(username=username, email=email)
    user.set_password(password)
    user.save()

    return JsonResponse({'message': 'User created successfully'}, status=201)


@require_POST
def username_validation(request):
    data = json.loads(request.body)
    username = data['username']

    if not str(username).isalnum():
        return JsonResponse({'username_error':'Username should only contain alphanumeric characters'}, status=400)

    if User.objects.filter(username=username).exists():
        return JsonResponse({'username_error':'Username is already taken '}, status=400)
   
    return JsonResponse({'username_valid':True})


@require_POST
def email_validation(request):
    data = json.loads(request.body)
    email = data['email']

    if not validate_email(email):
        return JsonResponse({'email_error':'Email Pattern Wrong'}, status=400)
    
    if User.objects.filter(email=email).exists():
        return JsonResponse({'email_error':'Email is already registered'},status=409)
    
    return JsonResponse({'email_valid':True})


@require_POST
def password_validation(request):
    data = json.loads(request.body)
    password1 = data['password1']
    password = data['password']

    if password != password1 :
        return JsonResponse({'password_error': 'Password doesnot match' }, status=400)
    
    return JsonResponse({'password_valid':True})

