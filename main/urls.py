from django.urls import path
#from . import views
from main import views

urlpatterns = [
    path('', views.index, name='home'),
    path('about', views.about, name='about'),
    path('auth', views.auth, name='auth'),
    path('registr', views.registr, name='registr'),
    path('user_info', views.user_info, name='user_info'),

]
