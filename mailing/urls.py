from django.urls import path
from mailing.apps import MailingConfig
from mailing.views import IndexView, MailingListView, UserLoginView, UserRegistrationView, UserLogoutView, \
    UserPasswordResetView, UserPasswordResetDoneView, UserPasswordResetConfirmView, UserPasswordResetCompleteView


app_name = MailingConfig.name

urlpatterns = [
    path('', IndexView.as_view()),
    path('registration/', UserRegistrationView.as_view(), name='registration'),
    path('mailing/', MailingListView.as_view(), name='mailing_list'),
    path('login/', UserLoginView.as_view(), name='login'),
    path('logout/', UserLogoutView.as_view(), name='logout'),
    path('password/reset/', UserPasswordResetView.as_view(), name='password_reset'),
    path('password/reset/done/', UserPasswordResetDoneView.as_view(), name='password_reset_done'),
    path('password/reset/confirm/<uidb64>/<token>/', UserPasswordResetConfirmView.as_view(),
         name='password_reset_confirm'),
    path('password/reset/complete/', UserPasswordResetCompleteView.as_view(), name='password_reset_complete'),
]
