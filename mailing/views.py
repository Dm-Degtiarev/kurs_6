from django.shortcuts import render
from django.views.generic import TemplateView


class IndexView(TemplateView):
    template_name = 'mailing/index.html'


class MailingListView(TemplateView):
    template_name = 'mailing/mailing_list.html'
