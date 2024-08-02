from django.urls import path
from django.views.decorators.csrf import csrf_exempt
from prediction import views

urlpatterns=[
    path('',views.index,name='index'),  
     path('submit/',views.submit,name='submit'),
]