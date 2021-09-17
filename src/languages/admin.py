from django.contrib import admin

from languages.models import Language


class LanguageAdmin(admin.ModelAdmin):
    list_display = ('name_native', 'name_en', 'slug')
    search_fields = ('name_en', 'slug')


admin.site.register(Language, LanguageAdmin)
