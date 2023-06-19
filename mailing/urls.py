from django.urls import path
from mailing.apps import MailingConfig
from mailing.views import IndexView, MailingListView, UserLoginView, UserRegistrationView


app_name = MailingConfig.name

urlpatterns = [
    path('', IndexView.as_view()),
    path('registration/', UserRegistrationView.as_view(), name='registration'),
    path('mailing/', MailingListView.as_view(), name='mailing_list'),
    path('login/', UserLoginView.as_view(), name='login'),
]
