"""
user admin

"""
from django.contrib import admin
from django.contrib.auth.admin  import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _
from zooApi import models

class UserAdmin(BaseUserAdmin):
    """define the admin pages for users"""

    ordering = ['id']
    list_display = ['name','email','phone_number']

    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        (
            _('Permissions'),

            {'fields': ('is_active', 'is_staff', 'is_superuser',), }

        ),

        (_('Important dates'), {'fields': ('last_login',)}),

    )

    readonly_fields = ('last_login',)

    add_fieldsets = (

        (None, {'classes': ('wide',),
                'fields': ('email',
                           'password1',
                           'password2',
                           'name',
                           'is_staff',
                           'is_superuser',
                           'is_active',),
                }),
    )

admin.site.register(models.User, UserAdmin)
