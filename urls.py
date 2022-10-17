from django.urls import path, include
from django.conf.urls.i18n import i18n_patterns
from django.contrib.auth import views as auth_views

from . import views
from . import forms

app_name = 'account'

urlpatterns = [
    path('signup/js/validate_email/', views.validate_create_account, name='validate_email'),
    path('create-account/js/validate_email/', views.validate_create_account),
    path('create-account/', views.create_account, name='create-account'),
    path('verify-email/', views.PostCreateAccount.as_view(), name='verify-email'),
    path('update-profile/', views.update_profile, name='update-profile'),
    path('login/', views.LoginPage.as_view() , name='login-account'),
    path('logout/', views.logout_account, name='logout-account'),    
]