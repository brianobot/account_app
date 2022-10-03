from django.views import generic
from django.http.response import HttpResponse, JsonResponse
from django.core.mail import send_mail, BadHeaderError
from django.db.models.query_utils import Q
from django.views.generic.base import TemplateView
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordResetForm
from django.contrib.auth.mixins import LoginRequiredMixin 
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth import views as auth_views
from django.contrib import messages
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.utils.translation import gettext_lazy as _
from django.urls import reverse_lazy 
from django.template.loader import render_to_string
from django.shortcuts import redirect, render
from .forms import AddressSelectionForm, CustomUserChangeForm, CustomUserCreationForm, AuthenticationForm, SimpleProfileSetting
from .models import User
from verify_email.email_handler import send_verification_email

import logging
logger = logging.getLogger(__name__)

# accounts views
def profile(request):
    return HttpResponse("Welcome to the profile page....")
 

def validate_create_account(request):
    """
    use with the javascript bal bla bla to validate unique email address
    """
    email = request.GET.get('email', None)
    data = {
        'is_taken': User.objects.filter(email__iexact=email).exists()
    }
    if data['is_taken']:
        data['error_message'] = 'A user with this email already exists.'
    
    return JsonResponse(data)

def create_account(request):
    if request.user.is_authenticated:
        return redirect('sales:homepage')
    else:
        if request.method == 'POST':
            form = CustomUserCreationForm(request.POST)
            print('about to check if the form is valid')
            if form.is_valid():
                print('the form is valid....')
                request.session['recent_email'] = form.cleaned_data.get('email')
                user_email = form.cleaned_data.get('email')
                # form.save()
                inactive_user = send_verification_email(request, form)
                messages.success(request, f'Account for <i><u>{user_email}</u></i> created Successfully')
                messages.info(request, f"Confirmation Link has been sent to <i><u>{user_email}</u></i>")
                logger.info(request, f'Account has been created for user with email = {user_email}')
                # send email/phone verification to user for account PIN verification
                # return redirect("account:login-account") #redirect now point to a blank page that tells the user to verify their account
                return redirect("account:verify-email")
            else:
                print('taking the else path....')
                return render(request, 'accounts/create_account.html', {"form": form})
        
        form = CustomUserCreationForm()
        previous_page = request.META.get('HTTP_REFERER')
        logger.info(f'account create page visited from {previous_page}')
        return render(request, 'accounts/create_account.html', {"form": form})


class PostCreateAccount(TemplateView):
    template_name = 'accounts/post_create_account.html'


class LoginPage(auth_views.LoginView):
    template_name = 'accounts/login.html'
    form_class = AuthenticationForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['email'] = self.request.session.get('recent_email')
        return context

    def get(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect('sales:homepage')
        previous_page = self.request.META.get('HTTP_REFERER')
        logger.info(f'account log-in page visited from {previous_page}')
        return super().get(*args, **kwargs)


#review this view function and rewrite as neccessary
@login_required(login_url='account:login-account')
def update_profile(request):
    if request.method == 'POST':
        form = CustomUserChangeForm(instance=request.user, data=request.POST, files=request.FILES)
        if form.is_valid():
            form.save()
            return redirect('sales:homepage')
    form = CustomUserChangeForm(instance=request.user)
    return render(request, 'accounts/update_account.html', {"form": form})


def logout_account(request):
    logout(request)
    return redirect('account:login-account')


def password_reset_request(request):
    if request.method == "POST":
        password_reset_form = PasswordResetForm(request.POST)
        if password_reset_form.is_valid():
            user_email = password_reset_form.cleaned_data['email']
            associated_users = User.objects.filter(email=user_email)
            if associated_users.exists():
                for user in associated_users:
                    subject = 'Password Reset Requested'
                    email_template_name = "accounts/password/password_reset_email.txt"
                    c = {
                        "email": user.email,
                        'domain':'127.0.0.1:8000',
                        'site_name': 'Website',
                        "uid": urlsafe_base64_encode(force_bytes(user.pk)),
                        "user": user,
                        'profile': str(user.profile).title,
                        'token': default_token_generator.make_token(user),
                        'protocol': 'http',
                    }
                    email = render_to_string(email_template_name, c)
                    try:
                        send_mail(subject, email, 'admin@example.com' , [user.email], fail_silently=False)
                    except BadHeaderError:
                        return HttpResponse('Invalid header found.')
                    return redirect("password_reset_done")

    password_reset_form = PasswordResetForm()
    return render(request, template_name="accounts/password/password_reset.html", context={"password_reset_form": password_reset_form})
