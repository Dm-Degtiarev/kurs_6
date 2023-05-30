from django.urls import path
from mailing.apps import MailingConfig
from mailing.views import IndexView, MailingListView


app_name = MailingConfig.name

urlpatterns = [
    path('', IndexView.as_view()),
    path('mailing/', MailingListView.as_view(), name='mailing_list')
]
