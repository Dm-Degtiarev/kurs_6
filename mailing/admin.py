from django.contrib import admin
from mailing.models import Mailing, User, Client, MailingMessage, MailingTrying


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('email', 'first_name', 'last_name', 'avatar', 'phone_number', 'country')
    search_fields = ('email', 'first_name', 'last_name', 'phone_number')
    list_filter = ('first_name', 'country')
    list_display_links = ('email',)

@admin.register(Client)
class Client(admin.ModelAdmin):
    list_display = ('email', 'fio', 'comment')
    search_fields = ('email', 'fio')
    list_filter = ('comment',)
    list_display_links = ('email',)

@admin.register(Mailing)
class MailingAdmin(admin.ModelAdmin):
    list_display = ('name', 'time', 'regularity', 'status', )
    search_fields = ('name',)
    list_filter = ('regularity', 'status', 'client')
    list_display_links = ('name',)

@admin.register(MailingMessage)
class MailingMessageAdmin(admin.ModelAdmin):
    list_display = ('topic', 'text')
    search_fields = ('topic',)
    list_filter = ('topic',)
    list_display_links = ('topic',)

@admin.register(MailingTrying)
class MailingTryingAdmin(admin.ModelAdmin):
    list_display = ('trying_date', 'mailing', 'status', 'server_response')
    search_fields = ('server_response',)
    list_filter = ('trying_date', 'status', 'server_response')