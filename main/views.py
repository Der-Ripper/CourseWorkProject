from django.shortcuts import render
from django.http import HttpResponse
from . import connection
# Create your views here.


def index(request):
    return render(request, 'main/index.html')

def about(request):
    return render(request, 'main/about.html')

def auth(request):
    return render(request, 'main/auth.html')

def registr(request):
    return render(request, 'main/registr.html')

def user_info(request):
    print(request.GET['uname'])
    print(request.GET['psw'])
    connection.select('Department')
    return HttpResponse('<h4>AAAAAAA</h4>')#render(request, 'main/registr.html')