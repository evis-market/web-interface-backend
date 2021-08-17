from django.contrib import admin
from django_admin_listfilter_dropdown.filters import DropdownFilter

from users.models import User


class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'first_name', 'last_name', 'email')
    search_fields = ('username', 'first_name', 'last_name', 'email')
    list_filter = (
        ('is_superuser', DropdownFilter),
    )


admin.site.register(User, UserAdmin)
