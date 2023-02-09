from django.urls import path

from . import views

urlpatterns = [
    path("api/v1/users/", views.UserView.as_view(), name="user_list"),
    path("api/v1/login/", views.LoginApiView.as_view(), name="login"),
    path("api/v1/signup/", views.SignupApiView.as_view(), name="signup"),
]