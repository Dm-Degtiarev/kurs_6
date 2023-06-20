from django.contrib.auth.views import LoginView, LogoutView, PasswordResetView, PasswordResetConfirmView, \
    PasswordResetDoneView, PasswordResetCompleteView
from django.shortcuts import render
from django.urls import reverse_lazy
from django.conf import settings
from django.views.generic import TemplateView, CreateView
from mailing.forms import UserAuthenticationForm, UserRegistartionForm, UserPasswordResetForm, UserResetConfirmForm


class UserLoginView(LoginView):
    form_class = UserAuthenticationForm
    template_name = 'mailing/user/user_login.html'
    extra_context = {
        'title': 'Авторизация'
    }

    def get_success_url(self):
        return reverse_lazy('mailing:mailing_list')

class UserLogoutView(LogoutView):
    next_page = reverse_lazy('mailing:login')


class UserRegistrationView(CreateView):
    form_class = UserRegistartionForm
    template_name = 'mailing/user/user_registration.html'
    success_url = reverse_lazy('mailing:login')
    extra_context = {
        'title': 'Регистрация'
    }

class UserPasswordResetView(PasswordResetView):
    form_class = UserPasswordResetForm
    template_name = 'mailing/user/user_password_reset_form.html'
    success_url = reverse_lazy('mailing:password_reset_done')
    email_template_name = 'mailing/user/user_email_reset.html'
    from_email = settings.EMAIL_HOST_USER
    extra_context = {
        'title': 'Восстановление пароля'
    }

class UserPasswordResetDoneView(PasswordResetDoneView):
    template_name = 'mailing/user/user_password_reset_done.html'
    extra_context = {
        'title': 'Письмо отправлено'
    }

class UserPasswordResetConfirmView(PasswordResetConfirmView):
    form_class = UserResetConfirmForm
    template_name = 'mailing/user/user_password_reset_confirm.html'
    success_url = reverse_lazy('mailing:password_reset_complete')
    extra_context = {
        'title': 'Новый пароль'
    }

class UserPasswordResetCompleteView(PasswordResetCompleteView):
    template_name = 'mailing/user/user_password_reset_complete.html'
    extra_context = {
        'title': 'Пароль изменен'
    }

class IndexView(TemplateView):
    template_name = 'mailing/index.html'
    extra_context = {
        "title": 'Главная'
    }

class MailingListView(TemplateView):
    template_name = 'mailing/mailing_list.html'
