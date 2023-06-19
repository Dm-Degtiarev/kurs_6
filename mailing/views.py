from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.views import LoginView
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import TemplateView, CreateView

from mailing.forms import UserAuthenticationForm, UserRegistartionForm


class UserLoginView(LoginView):
    form_class = UserAuthenticationForm
    template_name = 'mailing/user/user_login.html'

    def get_success_url(self):
        return reverse_lazy('mailing:mailing_list')

class UserRegistrationView(CreateView):
    form_class = UserRegistartionForm
    template_name = 'mailing/user/user_registration.html'
    success_url = reverse_lazy('mailing:login')


class IndexView(TemplateView):
    template_name = 'mailing/index.html'


class MailingListView(TemplateView):
    template_name = 'mailing/mailing_list.html'
