"""Custom User and profiles admin site models."""
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from users.models import CustomerProfile, User, VendorProfile
from users.user_forms import CustomUserCreationForm, CustomUserChangeForm
from users.vendor_forms import VendorCreationForm, VendorChangeForm
from users.customer_forms import CustomerChangeForm, CustomerCreationForm


class ProfileAdmin(admin.ModelAdmin):
    """Profile common admin configrations."""

    def get_user(self, obj):
        """Return the profile user."""
        return obj.user
    get_user.admin_order_field = 'user'
    get_user.short_description = 'User'

    def get_form(self, request, obj=None, **kwargs):
        """Assign the right form based on the existance of user instance."""
        if not obj:
            self.form = self.add_form
        else:
            self.form = self.change_form

        return super(ProfileAdmin, self).get_form(request, obj, **kwargs)

    def save_model(self, request, obj, form, change):
        """Given a model instance save it to the database."""
        obj.user.save()
        obj.save()

    def delete_model(self, request, obj):
        """Given a model instance delete it from the database."""
        user = obj.user
        obj.delete()
        user.delete()

    def delete_queryset(self, request, queryset):
        """Given a queryset, delete it from the database."""
        for profile in queryset:
            user = profile.user
            profile.delete()
            user.delete()


class VendorAdmin(ProfileAdmin):
    """Vendor Profile admin configration."""

    model = VendorProfile
    list_display = ('get_user',)
    change_form = VendorChangeForm
    add_form = VendorCreationForm


class CustomerAdmin(ProfileAdmin):
    """Customer Profile admin configration."""

    model = CustomerProfile
    list_display = ('get_user',)
    change_form = CustomerChangeForm
    add_form = CustomerCreationForm


class UserAdmin(BaseUserAdmin):
    """User admin configration."""

    model = User
    ordering = ('email',)
    form = CustomUserChangeForm
    add_form = CustomUserCreationForm
    list_display = ('email', 'is_staff', 'is_active', 'is_superuser',
                    'is_customer', 'is_vendor')

    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Permissions', {'fields': (
            'is_active', 'is_staff', 'is_superuser', 'is_customer', 'is_vendor'
        )}),
    )
    list_filter = ('is_staff', 'is_customer', 'is_vendor')
    # add_fieldsets is not a standard ModelAdmin attribute. UserAdmin
    # overrides get_fieldsets to use this attribute when creating a user.
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2'),
        }),
        ('Permissions', {'fields': ('is_staff', 'is_superuser')}),
    )
    search_fields = ('email',)
    ordering = ('email',)
    filter_horizontal = ()


admin.site.register(User, UserAdmin)
admin.site.register(VendorProfile, VendorAdmin)
admin.site.register(CustomerProfile, CustomerAdmin)
