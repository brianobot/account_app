from django.urls import path

from . import views

app_name = 'accounts'

urlpatterns = [
    path('signup/js/validate_email/', views.validate_create_account, name='validate_email'),
    path('create-account/js/validate_email/', views.validate_create_account),
    path('create-account/', views.create_account, name='create-account'),
    path('verify-email/', views.PostCreateAccount.as_view(), name='verify-email'),
    path('login/', views.LoginPage.as_view() , name='login-account'),
    path('logout/', views.logout_account, name='logout-account'),    
]