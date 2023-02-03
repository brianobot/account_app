from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from leaflet.admin import LeafletGeoAdmin, LeafletGeoAdminMixin
from .models import AccountBalance, User, Profile
from .forms import CustomUserCreationForm, CustomUserChangeForm 

# to be used within the UserAdmin admin page
class ProfileInline(LeafletGeoAdminMixin, admin.StackedInline):
    model = Profile
    extra = 0
    
# register out own model admin, based pn the default UserAdmin
@admin.register(User)
class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    # model = models.User
    list_display = ('email', 'first_name', 'last_name', 'is_staff', 'is_active',)
    list_filter =  ('email', 'first_name', 'last_name', 'is_staff', 'is_active', )
    
    fieldsets = (
        (None,          {'fields': ('email', 'password')}),
        ('Permissions', {'fields': ('is_staff', 'is_active')}),
        ('Names',       {'fields': ('first_name', 'last_name')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', 'is_staff', 'is_active')
        }),
    )
    search_fields = ('email',)
    ordering = ('email',)
    inlines = [ProfileInline]

@admin.register(AccountBalance)
class AccountBalanceAdmin(admin.ModelAdmin):
    list_display = ['profile', 'balance', 'currency']
    readonly_fields = ["profile", "balance", "currency"]