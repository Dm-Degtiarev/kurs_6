from django.contrib import admin
from mailing.models import Mailing, User


@admin.register(User)
class UserAdmib(admin.ModelAdmin):
    list_display = ('email', 'first_name', 'last_name', 'country')

@admin.register(Mailing)
class MailingAdmib(admin.ModelAdmin):
    list_display = ('name', 'time', 'regularity', 'status', )
    search_fields = ('name',)
    list_filter = ('regularity', 'status', 'client')
    list_display_links = ('name',)