from django.contrib import admin
from django_admin_listfilter_dropdown.filters import DropdownFilter

from users.models import User


class UserAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'email', 'phone', 'wallet_erc20')
    search_fields = ('first_name', 'last_name', 'email', 'phone', 'wallet_erc20')
    list_filter = (
        ('is_superuser', DropdownFilter),
    )


admin.site.register(User, UserAdmin)
