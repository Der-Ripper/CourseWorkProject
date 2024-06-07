from django.urls import include, path
#from . import views
from main import views
from django.contrib.auth import views as v

urlpatterns = [
    path('', views.index, name='home'),
    path('about', views.about, name='about'),
    path('auth', views.auth, name='auth'),
    path('registr', views.registr, name='registr'),
    path('registr_action', views.registr_action, name='registr_action'),
    path('user_info', views.user_info, name='user_info'),
    path('claim', views.claim, name='claim'),
    path('send_claim', views.send_claim, name='send_claim'),
    path('login/', views.login_view, name='login'),
    path('signup/', views.signup_view, name='signup'),
    path('logout/', views.logout_view, name='logout'),
    path('watch_claims', views.watch_claims, name='watch_claims'),
    path('new_claim', views.new_claim, name='new_claim'),
    path('branch_claims/', views.branch_claims, name='branch_claims'),
    path('department_claims/', views.department_claims, name='department_claims'),
]
