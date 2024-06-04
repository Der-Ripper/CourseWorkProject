from django.urls import path
#from . import views
from main import views

urlpatterns = [
    path('', views.index, name='home'),
    path('about', views.about, name='about'),
    path('auth', views.auth, name='auth'),
    path('registr', views.registr, name='registr'),
    path('registr_action', views.registr_action, name='registr_action'),
    path('user_info', views.user_info, name='user_info'),
    path('claim', views.claim, name='claim'),
    path('send_claim', views.send_claim, name='send_claim'),

]
