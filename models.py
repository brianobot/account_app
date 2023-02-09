from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.contrib.gis.db import models as gis_models
from django.utils.translation import gettext_lazy as _

from config.models import CurrencyMixin
from .managers import CustomUserManager

import logging
logger = logging.getLogger(__name__)


class User(AbstractUser):
    email = models.EmailField('email address', unique=True)
    ref = models.ForeignKey("self", on_delete=models.SET_NULL, blank=True, null=True)
    username = None

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    # prevents a user from been irrevesibly deleted from the database
    # on delete simply set the user to in-active
    def delete(self, *args, **kwargs):
        self.is_active = False
        self.save()

    def __str__(self) -> str:
        return str(self.email)

    def __repr__(self) -> str:
        return f"User(email='{self.email}', ref={self.ref})"


class Profile(models.Model):
    GENDER = (
        ('male', 'male'),
        ('female', 'female'),
    )

    """  
    this model repr the database table that will hold all non-authentication essential 
    details about a user, from preferences to accounts settings 
    """    
    bio = models.TextField(blank=True, null=True)
    handle = models.CharField(max_length=100, blank=True, null=True)
    uid = models.CharField(max_length=100, blank=True, null=True)
    gender = models.CharField(choices=GENDER, max_length=6, blank=True, null=True)
    avatar = models.ImageField(upload_to='avatars/', blank=True, default='avatars/blank_profile.png')
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, primary_key=True)
    location = gis_models.PointField(blank=True, null=True)

    is_verified = models.BooleanField(default=False, blank=True)

    @property
    def get_balance(self):
        return self.account_balance.balance

    def save(self, *args, **kwargs):
        if not self.handle:
            self.handle = "@" + self.user.email.split("@")[0]
        super().save(*args, **kwargs)

    def __str__(self):
        return str(self.handle)

    def __repr__(self):
        return f'<Profile(email={self.handle})>'    
    

class AccountBalance(CurrencyMixin):
    STATUS = (
        ('active', 'active'),
        ('inactive', 'inactive'),
        ('suspended', 'suspended'),
    )
    profile = models.OneToOneField(Profile, on_delete=models.CASCADE, null=True, related_name='account_balance')
    balance = models.DecimalField(default=0.0, max_digits=15, decimal_places=2 , blank=True, editable=False)
    status = models.CharField(max_length=20, choices=STATUS, default='active', blank=True)

    def top_up(self, transaction):
        if transaction.status != 'pending':
            raise AttributeError(f"Can not process the given transaction, status='{transaction.status}'")
        self.balance += transaction.net_amount
        self.save()

    def __str__(self):
        return str(self.profile)

    def __repr__(self):
        return f"AccountBalance(profile={self.profile}, currency={self.currency})"
