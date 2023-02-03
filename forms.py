from django import forms
from django.contrib import messages
from django.contrib.auth import authenticate
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from accounts.models import Profile, User

import logging
logger = logging.getLogger(__name__)

class CustomUserCreationForm(UserCreationForm):
    """ 
    Extends the UserCreationForm to add the email field as a field to be used in the form
    """
    error_css_class = 'error'
    required_css_class = 'required'

    USER_TYPE = (('vendor', 'vendor'),('user', 'user'))
    user_type = forms.ChoiceField(choices=USER_TYPE, required=False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # this widgets attributes are set here because modelforms won't recognize fields declared in the modelforms itself
        self.fields['password1'].widget.attrs['placeholder'] = 'Password'
        self.fields['password2'].widget.attrs['placeholder'] = 'Confirm Password'
        self.fields['password1'].widget.attrs['class'] = 'form-control'
        self.fields['password2'].widget.attrs['class'] = 'form-control'
        self.fields['password1'].widget.attrs['arial-label'] = 'Password'
        self.fields['password2'].widget.attrs['arial-label'] = 'Confirm Password'

    class Meta(UserCreationForm.Meta):
        model = User
        # review - pack the minimal no of fields to get just enuf data about a useron creation
        fields = ('email',)        

        widgets = {
            "email": forms.EmailInput(attrs={"class": "form-control", 'placeholder': 'Email', 'auto-complete': 'off'}),
        }

    def send_sms(self):
        # TODO: review implement sms sending to users to alert and welcome them to the system
        pass

    def clean(self):
        email = self.cleaned_data.get('email')
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if (email is not None) and (password1 is not None) and (password2 is not None):
            used_email = User.objects.filter(email=email).exists()
            if used_email:
                raise forms.ValidationError("Email has already been used")
        return self.cleaned_data


class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = User
        fields = ('email',)


class AuthenticationForm(forms.Form):
    """
    Form to authenticate a valid user into the system/platform
    """
    email = forms.EmailField(max_length=255, help_text=_('Enter Email address'), label="Email address", 
            widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email address', 'auto-complete': 'off'}))
    password = forms.CharField(min_length=5, max_length=255, strip=False, help_text=_('Enter Password'), 
            widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password', 'auto-complete': 'off'}))

    widgets = {
        'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email address', 'auto-complete': 'off'}),
        'password': forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password', 'auto-complete': 'off'}),
    }

    def __init__(self, request, *args, **kwargs):
        self.request = request
        self.user = None
        super().__init__(*args, **kwargs)

    def clean(self):
        email = self.cleaned_data.get('email')
        password = self.cleaned_data.get('password')
        
        if email is not None and password:
            self.user = authenticate(self.request, email=email, password=password) 

            if self.user is None:
                logger.warn(f"Authentication failed for email = {email or 'blank'}")
                raise ValidationError("Invalid email and password combination")
            logger.info(f"Authentication successful for email = {email}")
            messages.success(self.request, f"Welcome back! it has been a minute... <a href='/explore'>check out what you missed 🔎</a>")
        
        return self.cleaned_data

    def get_user(self):
        return self.user

    # TODO: check the usefulness of this Meta class declaration here, since this is Form and not a ModelForm
    class Meta:
        model = Profile
        fields = ('handle', 'avatar')