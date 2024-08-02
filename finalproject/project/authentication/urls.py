from django.urls import path
from django.views.decorators.csrf import csrf_exempt
from authentication import views

urlpatterns=[
    path('register/',views.Registration,name='register'),
    path('login/',views.Login,name='login'),
    path('logout/',views.Logout,name='logout'),
    path('validation-username/',csrf_exempt(views.username_validation),name='validation-username'),
    path('registration_api/',csrf_exempt(views.registration_api),name='registration_api'),
    path('login_api/',csrf_exempt(views.login_api),name='login_api'),
    path('validation-password/',csrf_exempt(views.password_validation),name='validation-password'),
    path('validation-email/',csrf_exempt(views.email_validation),name='validation-email'),  
    path('login/',views.Login,name='login'),
]