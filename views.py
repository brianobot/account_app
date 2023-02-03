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
from django.shortcuts import redirect, render
from django.conf import settings
from django.template.loader import render_to_string
from .forms import CustomUserChangeForm, CustomUserCreationForm, AuthenticationForm
from .models import User

import logging
logger = logging.getLogger(__name__)


def validate_create_account(request):
    """
    use with the javascript (ajax call) to validate unique email address
    """
    email = request.GET.get('email', None)
    data = {
        'is_taken': User.objects.filter(email__iexact=email).exists(),
        'error_message': None,
    }
    if data['is_taken']:
        data['error_message'] = 'A user with this email already exists.'
    
    return JsonResponse(data)


def create_account(request):
    if request.user.is_authenticated:
        return redirect('ticket:homepage')
    else:
        if request.method == 'POST':
            form = CustomUserCreationForm(request.POST)
            if form.is_valid():
                request.session['recent_email'] = form.cleaned_data.get('email')
                user_email = form.cleaned_data.get('email')
                user = form.save()
                messages.success(request, f'Account for <i><u>{user_email}</u></i> created Successfully')
                messages.info(request, f"Confirmation Link has been sent to <i><u>{user_email}</u></i>")
                logger.info(request, f'Account has been created for user with email = {user_email}')
                # send email/phone verification to user for account PIN verification

                email_template = 'account/email/welcome_message.html'
                email_context = {'name': user_email, 'social_links': 'http://127.0.0.1:8000/about/#social-section'}
                subject = 'Welcome to the Platform'
                message = render_to_string(email_template, email_context)
                sender = settings.EMAIL_HOST_USER
                receipient = [user_email]
                send_mail(subject, message, sender, receipient, fail_silently=True)
            
                return redirect("accounts:login-account")
            
        else:
            form = CustomUserCreationForm()
            
        previous_page = request.META.get('HTTP_REFERER')
        logger.info(f'account create page visited from {previous_page}')
        return render(request, 'account/signup.html', {"form": form})


class PostCreateAccount(TemplateView):
    template_name = 'account/post_create_account.html'


class LoginPage(auth_views.LoginView):
    template_name = 'account/login.html'
    form_class = AuthenticationForm

    def get(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect('ticket:homepage')
        previous_page = self.request.META.get('HTTP_REFERER')
        logger.info(f'account log-in page visited from {previous_page}')
        return super().get(*args, **kwargs)


def logout_account(request):
    logout(request)
    return redirect('accounts:login-account')


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
                    email_context = {
                        "email": user.email,
                        'domain':'127.0.0.1:8000',
                        'site_name': 'Website',
                        "uid": urlsafe_base64_encode(force_bytes(user.pk)),
                        "user": user,
                        'profile': str(user.profile).title,
                        'token': default_token_generator.make_token(user),
                        'protocol': 'http',
                    }
                    body = render_to_string(email_template_name, email_context)
                    try:
                        send_mail(subject, body, 'admin@example.com' , [user.email], fail_silently=False)
                    except BadHeaderError:
                        return HttpResponse('Invalid header found.')
                    return redirect("password_reset_done")
    else:
        password_reset_form = PasswordResetForm()
    return render(request, template_name="accounts/password/password_reset.html", context={"password_reset_form": password_reset_form})
