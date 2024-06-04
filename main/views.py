from django.shortcuts import render
from django.http import HttpResponse
from . import connection
from django.contrib.auth.decorators import login_required
# Create your views here.


def index(request):
    return render(request, 'main/index.html')

def about(request):
    return render(request, 'main/about.html')

def auth(request):
    return render(request, 'main/auth.html')

def registr(request):
    return render(request, 'main/registr.html')

def claim(request):
    return render(request, 'main/claim.html')

def send_claim(request):
    print(request.GET)
    pory = request.GET['phy_or_yur']
    name = request.GET['name']
    age = request.GET['age']
    living_address = {'street':request.GET['living_address_street'], 'house': request.GET['living_address_house']}
    registration_address = {'street':request.GET['registration_address_street'], 'house': request.GET['registration_address_house']}
    email = request.GET['email']
    phone = request.GET['phone']
    inn = request.GET['inn']
    passport = request.GET['passport']
    title = request.GET['title']
    description = {'text': request.GET['description']}
    print(pory, name, age, living_address, registration_address, email, phone, inn, passport, title, description)
    if pory == '1':
        print('\n\nQQQQQQQQQQQQQQQQQQQQQQQQQQQQ\n\n')
        connection.test_procedure(name, age, living_address, registration_address, email, phone, inn, passport, title, description)
    return HttpResponse('<h4>121212121</h4>')#render(request, 'main/cliam.html')

def registr_action(request):
    print(request.GET)
    print(request.GET['phy_or_yur'])
    return HttpResponse('<h4>БББББББББББ</h4>')#render(request, 'main/registr_physic.html')

def user_info(request):
    print(request.GET['uname'])
    print(request.GET['psw'])
    user = connection.client_auth(request.GET['uname'], request.GET['psw'])
    if user:
        user_data = {}
        user_data['name'] = user[1]
        user_data['age'] = user[2]
        user_data['email'] = user[5]  
        user_data['phy_or_yur'] = 2#user[5]       
        print(user)
        return render(request, 'main/physic_info.html', user_data)
        #return HttpResponse('<h4>Ты норм чел, все гуд</h4>')
    return HttpResponse('<h4>Ты че балда?</h4>')#render(request, 'main/registr.html')