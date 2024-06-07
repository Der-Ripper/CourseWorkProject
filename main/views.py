from django.http import HttpResponse

from main.models import Claim
from . import connection
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.contrib.auth import get_user_model
from django.shortcuts import render, redirect
from django.contrib.auth import views
from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import logout
from django.contrib import messages
# Create your views here.

User = get_user_model()

def login_as_user(request, user_id):
    # Убедитесь, что пользователь существует
    try:
        user = User.objects.get(id=user_id)
    except User.DoesNotExist:
        return redirect('404')
    
    # Получаем сессионный ключ пользователя
    session_key = user.session_key
    
    # Авторизуемся под этим пользователем
    request.session['_auth_user_backend'] = 'django.contrib.auth.backends.ModelBackend'
    request.session['_auth_user_id'] = str(user.id)
    request.session['_auth_user_hash'] = request.session.get('_auth_user_hash', '')
    request.session.save()
    
    # Перенаправляем пользователя на главную страницу
    return redirect('home')

def logout_user(request):
    auth_logout(request)
    return redirect('home')

# Функция для создания нового пользователя
def create_new_user():
    new_user = User.objects.create_user('username', 'email@example.com', 'password')
    return new_user

# Функция для получения сессионного ключа нового пользователя
def get_session_key_for_new_user():
    new_user = create_new_user()
    return new_user.session_key

def index(request):
    username = request.session.get('post_login')
    password = request.session.get('post_password')
    userDB = connection.auth_via_db(username, password)
    user_data = {}
    if userDB:
        if len(userDB) < 12:
            print('\n\n\n1111')
            user_data['role'] = 1
        else:
            if userDB[2] == 1:
                user_data['role'] = 2
            elif userDB[2] == 2:
                user_data['role'] = 3
    return render(request, 'main/index.html', {'user_data': user_data})

def about(request):
    username = request.session.get('post_login')
    password = request.session.get('post_password')
    userDB = connection.auth_via_db(username, password)
    user_data = {}
    if userDB:
        if len(userDB) < 12:
            print('\n\n\nABOUT - 1111')
            user_data['role'] = 1
        else:
            print(userDB[2])
            if userDB[2] == 1:
                user_data['role'] = 2
            elif userDB[2] == 2:
                user_data['role'] = 3
    return render(request, 'main/about.html', {'user_data': user_data})

def auth(request):
    return render(request, 'main/auth.html')

def registr(request):
    return render(request, 'main/registr.html')

@login_required
def watch_claims(request):
    print('USER:', request.user)
    claims = connection.select_all_client_claims(str(request.user))
    if claims and len(claims) > 0:
        claim_data = {}
        claim = claims[-1]
        claim_data['id'] = claim[11]
        claim_data['status'] = claim[10]
        claim_data['name'] = claim[0]
        claim_data['age'] = claim[1]
        claim_data['title'] = claim[8]
        if claim[9] is None:
            claim_data['description'] = 'Пусто'
        else:
            claim_data['description'] = claim[9]['text']
    return render(request, 'main/watch_claims.html', {'claim_data':claim_data})

@login_required
def claims_of_department(request):
    print('USER:', request.user)
    connection.select_branch_claims(str(request.user))
    return render(request, 'main/branch_claims.html')

@login_required
def new_claim(request):
    print('USER:', request.user)
    claims = connection.select_all_client_claims(str(request.user))
    if claims and len(claims) > 0:
        claim = claims[-1]
        print('CLAIM:', claim)
        claim_data = {}
        claim_data['id'] = claim[11]
        claim_data['status'] = claim[10]
        claim_data['title'] = claim[8]
        if claim[9] is None:
            claim_data['description'] = 'Пусто'
        else:
            claim_data['description'] = claim[9]['text']
        return render(request, 'main/new_claim.html', {'claim': claim_data})
    else:
        return redirect('home')

@login_required
def claim(request):
    #pory = request.session.get('pory')
    #print('\n\nPORY\n\n', pory)
    print('\nMETHOD\n', request.method)
    if request.method == 'POST':
        #username = request.POST.get('username')
        #password = request.POST.get('password')
        username = request.session.get('post_login')
        password = request.session.get('post_password')
        user = connection.auth_via_db(username, password)
        user_data = {}
        if user:
            if request.user.check_password(password):
                print('QQQQQQQQ:', user)
                user_data['pory'] = user[9]
                print(user_data)
                return render(request, 'main/claim.html', {'user_data': user_data})
                #return render(request, 'main/claim.html', user_data)
            else:
                messages.error(request, 'Invalid password')
        else:
            messages.error(request, 'User not found')
    return render(request, 'main/claim.html')

'''
@login_required
def claim_bad(request):
    #print('QQ', request.GET)
    #print('UNAME:', request.GET['uname'])
    #print('PSW:', request.GET['psw'])
    print('USER:', request.user)
    user = connection.select_user_via_login_and_password(str(request.user))
    user_data = {}
    if user:
        user_data['pory'] = user[9]
    return render(request, 'main/claim.html', user_data)
'''

def send_claim(request):
    print(request.GET)
    name = request.GET['name']
    age = request.GET['age']
    living_address = {'street':request.GET['living_address_street'], 'house': request.GET['living_address_house']}
    registration_address = {'street':request.GET['registration_address_street'], 'house': request.GET['registration_address_house']}
    email = request.GET['email']
    phone = request.GET['phone']
    inn = request.GET['inn']
    title = request.GET['title']
    description = {'text': request.GET['description']}
    if request.GET.get('passport'):
        passport = request.GET['passport']
        if connection.test_procedure(name, age, living_address, registration_address, email, phone, inn, passport, title, description, str(request.user)):
            return redirect('new_claim') 
        else:
            return redirect('claim')
    else:
        if (request.GET.get('kpp') and request.GET.get('ogrn') and request.GET.get('okved')) :
            kpp = request.GET['kpp']
            ogrn = request.GET['ogrn']
            okved = request.GET['okved']
            if connection.registration_client_yur(name, age, living_address, registration_address, email, phone, inn, ogrn, kpp, okved, title, description, str(request.user)):
                return redirect('new_claim') 
            else:
                return redirect('claim')

    #return HttpResponse('<h4>121212121</h4>')#render(request, 'main/cliam.html')

def registr_action(request):
    print(request.GET)
    print(request.GET['phy_or_yur'])
    user = User.objects.create_user(username=request.GET['email'], email=request.GET['email'], password=request.GET['psw'])
    user = authenticate(username=request.GET['email'], password=request.GET['psw'])
    user.save()
    print(user)
    return HttpResponse('<h4>БББББББББББ</h4>')#render(request, 'main/registr_physic.html')


@login_required
def user_info(request):
    username = request.session.get('post_login')
    password = request.session.get('post_password')
    if username and password:
        # Выполните необходимые действия с username и password
        user = connection.auth_via_db(username, password)
        print('SESSION-UNAME:', username)
        print('SESSION-PSW', password)
        # Очистка данных из сессии после использования
        #del request.session['post_login']
        #del request.session['post_password']
        if user:
            user_data = {}
            user_data['id'] = user[0]
            user_data['name'] = user[1]
            user_data['age'] = user[2]
            if user[3] is None:
                user_data['alstreet'] = 'Неизвестно'
                user_data['alhouse'] = 'Неизвестно'
            else:
                user_data['alstreet'] = user[3]['street']
                user_data['alhouse'] = user[3]['house']

            if user[4] is None:
                user_data['arstreet'] = 'Неизвестно'
                user_data['arhouse'] = 'Неизвестно'
            else:
                user_data['arstreet'] = user[4]['street']
                user_data['arhouse'] = user[4]['house']
            user_data['email'] = user[5]  
            user_data['phone'] = user[6]  
            user_data['login'] = user[7]
            user_data['phy_or_yur'] = user[9]
            #request.session['pory'] = user[9]
            print(user_data)
            return render(request, 'main/physic_info.html', {'user': user_data})
        else:
            return render(request, 'registration/login.html', {'form': LoginForm()})
    return render(request, 'registration/login.html', {'form': LoginForm()})

'''
@login_required
def user_info_middle(request):
    print('REQUEST METHOD:', request.method)
    if request.method == 'POST':
        form = LoginForm(request.POST)
        print('FORM POSTED:', form)
        if form.is_valid():
            print('FORM IS VALID')
            login = form.cleaned_data['login']
            password = form.cleaned_data['password']
            user = connection.select_user_via_login_and_password(login, password)
            if user:
                if request.user.check_password(password):
                    # Ваш код для обработки пользователя
                    return render(request, 'main/physic_info.html', {'user': user, 'form': form})
                else:
                    messages.error(request, 'Invalid password')
            else:
                messages.error(request, 'User not found')
        else:
            messages.error(request, 'Invalid form data')
    else:
        form = LoginForm()

    return render(request, 'main/physic_info.html', {'form': form})

@login_required
def user_info_bad(request):
    print('::: 1')
    print(request.method)
    if request.method == 'POST':
        print('::: 2')
        form = LoginForm(request.POST)
        if form.is_valid():
            login = form.cleaned_data['login']
            password = form.cleaned_data['password']
            print('USER:', request.user)
            print('IS_AUTH:', request.user.is_authenticated)
            user = connection.select_user_via_login_and_password(login, password)
            if user:
                if request.user.check_password(password):
                    user_data = {}
                    user_data['name'] = user[1]
                    user_data['age'] = user[2]
                    user_data['email'] = user[5]  
                    user_data['phy_or_yur'] = user[9]
                    print('USER_DATA:', user_data)
                    return render(request, 'main/physic_info.html', user_data)
                else:
                    messages.error(request, 'Invalid password')
        else:
            messages.error(request, 'Invalid form data')
    else:
        print('>>> 2')

        form = LoginForm()
    return render(request, 'main/physic_info.html', {'form': form})

    if user:
        if request.user.check_password(user[8]):
            print(user[8])
            print(request.user.check_password(user[8]))
            user_data = {}
            user_data['name'] = user[1]
            user_data['age'] = user[2]
            user_data['email'] = user[5]  
            user_data['phy_or_yur'] = user[9]
            return render(request, 'main/physic_info.html', user_data)
    return HttpResponse('<h4>Ты че балда?</h4>')#render(request, 'main/registr.html')
'''


class LoginUser(views.LoginView):
    form_class = AuthenticationForm
    template_name = 'main/auth.html'
 
    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="Авторизация")
        return dict(list(context.items()) + list(c_def.items()))
    

def login_view(request):
    if request.method == 'POST':
        form = LoginForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            userDB = connection.auth_via_db(username, password)
            print('\nUSERDB:\n', userDB)
            if userDB:
                user = authenticate(username=username, password=password)
                print(user)
                if user is not None:
                    login(request, user)
                    request.session['post_login'] = username
                    request.session['post_password'] = password
                    if len(userDB) < 12:
                        return redirect('user_info')  # Перенаправление на домашнюю страницу или любую другую
                    else:
                        if userDB[2] == 1:
                            return redirect('branch_claims')
                        elif userDB[2] == 2:
                            return redirect('department_claims')                            
            else:
                form = LoginForm()
    else:
        form = LoginForm()
    return render(request, 'registration/login.html', {'form': form})

def signup_view(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            switch_value = form.cleaned_data.get('switch')
            # Сделайте что-нибудь с переменной switch_value, если нужно
            #user = authenticate(username=username, password=password)
            #login(request, user)
            #return HttpResponse('<h4>87879</h4>')#redirect('user_info') 
            #Сюда часть, отвечающую за вызов процедуры регистрации уродца
            if connection.registration_client(str(username), str(password), int(switch_value)):
                print('Тут тебя не должно быть')
                user = authenticate(username=username, password=password)
                print('Тут тебя не должно быть - 2')
                
                login(request, user)
                print('Тут тебя не должно быть - 3')
                request.session['post_login'] = username
                request.session['post_password'] = password
                return redirect('user_info')  # Перенаправление на домашнюю страницу или любую другую
            else:
                print('\n\nНе получилось\n\n')
                form = SignUpForm()
    else:
        form = SignUpForm()
    return render(request, 'registration/signup.html', {'form': form})

def logout_view(request):
    logout(request)
    #del request.session['post_login']
    #del request.session['post_password']
    return redirect('home')

@login_required
def branch_claims(request):
    print('\n\nFFFFFFFFFFFFFFfF\n\n')
    username = request.session.get('post_login')
    password = request.session.get('post_password')
    userDB = connection.auth_via_db(username, password)
    print('\n\nLLLLLLLLLLLLLLLLLl\n\n')
    if userDB:
        if len(userDB) < 12:
            return redirect('home')
        else:
            if userDB[2] == 1:
                claims = connection.select_all_branch_claims()
                claims_data = []
                for claim in claims:
                    claim_data = {}
                    claim_data['number'] = claim[0]
                    claim_data['status'] = claim[1]
                    claim_data['name'] = claim[2]
                    claims_data.append(claim_data)
                return render(request, 'main/branch_claims.html', {'claims_data': claims_data})
                #return redirect('branch_claims') # Перенаправление после успешного сохранения
            else:
                return redirect('home')


@login_required
def department_claims(request):
    print('\n\nOOOOOOOOO\n\n')
    username = request.session.get('post_login')
    password = request.session.get('post_password')
    userDB = connection.auth_via_db(username, password)
    claims = []#Claim.objects.filter(client=request.user.client)  # Предположим, что у пользователя есть связанный объект Client
    print('\n\nLAAAAAAAAA\n\n')
    if userDB:
        if len(userDB) < 12:
            return redirect('home')
        else:
            if userDB[2] == 2:
                for claim in claims:
                    form = ClaimForm(request.POST, instance=claim)
                    if form.is_valid():
                        form.save()
                return render(request, 'main/department_claims.html')
                #return redirect('department_claims')  # Перенаправление после успешного сохранения
            else:
                redirect('home')

class LoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))

'''
class SignUpForm(UserCreationForm):
    #email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={'class': 'form-control'}))

    class Meta:
        model = User
        #fields = ('username', 'email', 'password1', 'password2')
        fields = ('username', 'password')

    def __init__(self, *args, **kwargs):
        super(SignUpForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({'class': 'form-control'})
        self.fields['password'].widget.attrs.update({'class': 'form-control'})
        #self.fields['password2'].widget.attrs.update({'class': 'form-control'})
'''

class SignUpForm(UserCreationForm):
    switch = forms.ChoiceField(
        choices=[(1, 'Физик'), (2, 'Юрик')],
        widget=forms.RadioSelect,
        initial=1
    )

    class Meta:
        model = User
        fields = ('username', 'password1', 'password2', 'switch')
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'password1': forms.PasswordInput(attrs={'class': 'form-control'}),
            'password2': forms.PasswordInput(attrs={'class': 'form-control'}),
        }

class ClaimForm(forms.ModelForm):
    class Meta:
        model = Claim
        fields = ['title', 'description', 'status', 'claim_number', 'department_name']